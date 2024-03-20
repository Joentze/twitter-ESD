package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB

type Like struct {
	UID       string    `json:"user id" db:"uid"`
	PostID    string    `json:"post id" db:"post_id"`
	DateLiked time.Time `json:"date liked" db:"date_liked"`
}

func initDB() *sql.DB {
	dbHost := os.Getenv("MYSQL_HOST")
	dbPort := os.Getenv("MYSQL_PORT")
	dbPwd := os.Getenv("MYSQL_ROOT_PASSWORD")

	dsn := "root:" + dbPwd + "@tcp(" + dbHost + ":" + dbPort + ")/twitter_app"
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal(err)
	}
	return db
}

func main() {
	db = initDB()
	defer db.Close()

	router := gin.Default()
	router.Use(CORSMiddleware())

	router.GET("/likes", getAllLikes)
	router.GET("/userLikes/:uid", getUserLikes)
	router.GET("/like/:post_id", getPostLikes)
	router.POST("/like/:post_id", createLike)
	router.DELETE("/like/:post_id", deleteLike)

	log.Println("Likes API is running at port 5103")
	router.Run(":5103")
}

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		c.Next()
	}
}

func getAllLikes(c *gin.Context) {
	var likes []Like
	rows, err := db.Query("SELECT * FROM LIKES")
	if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"message": err.Error()})
		return
	}
	defer rows.Close()

    for rows.Next() {
        var l Like
        var dateLikedStr string // Assuming the date_liked column is stored as a string in the database

        err := rows.Scan(&l.UID, &l.PostID, &dateLikedStr)
        if err != nil {
            log.Println("Error scanning row:", err)
            continue
        }

        // Parse the dateLikedStr into a time.Time object
        l.DateLiked, err = time.Parse("2006-01-02 15:04:05", dateLikedStr)
        if err != nil {
            log.Println("Error parsing date:", err)
            continue
        }

        likes = append(likes, l)
    }

    if len(likes) == 0 {
        c.JSON(http.StatusOK, gin.H{
            "code": 200,
            "message": "No one is liking each other!",
        })
    } else {
        c.JSON(http.StatusOK, gin.H{
            "code": 200,
            "data": gin.H{
                "likes": likes,
            },
        })
    }
}

func getUserLikes(c *gin.Context) {
	uid := c.Param("uid")
	rows, err := db.Query("SELECT post_id FROM LIKES WHERE uid=?", uid)
	if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"message": err.Error()})
		return
	}
	defer rows.Close()

	var likes []string
	for rows.Next() {
		var postID string
		err := rows.Scan(&postID)
		if err != nil {
			log.Println(err)
			continue
		}
		likes = append(likes, postID)
	}

    if len(likes) == 0 {
        c.JSON(http.StatusOK, gin.H{
            "code": 200,
            "message": "User has not liked any posts!",
        })
    } else {
        c.JSON(http.StatusOK, gin.H{
            "code": 200,
            "data": likes,
        })
    }
}

func getPostLikes(c *gin.Context) {
	postID := c.Param("post_id")
	rows, err := db.Query("SELECT uid FROM LIKES WHERE post_id=?", postID)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"message": err.Error()})
        return
    }
	defer rows.Close()

	var likes []string
	for rows.Next() {
		var uid string
		err := rows.Scan(&uid)
		if err != nil {
			log.Println(err)
			continue
		}
		likes = append(likes, uid)
	}

    if len(likes) == 0 {
        c.JSON(http.StatusOK, gin.H{
            "code": 200,
            "message": "Post has no likes",
        })
    } else {
        c.JSON(http.StatusOK, gin.H{
            "code": 200,
            "data": likes,
        })
    }
}

func createLike(c *gin.Context) {
	postID := c.Param("post_id")
	var data map[string]string
	if err := c.BindJSON(&data); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	uid := data["uid"]
    var existing Like
    var existingDate string
    err := db.QueryRow("SELECT uid, post_id, date_liked FROM LIKES WHERE uid = ? AND post_id = ?", uid, postID).Scan(&existing.UID, &existing.PostID, &existingDate)
    if err == nil {
        existing.DateLiked, err = time.Parse("2006-01-02 15:04:05", existingDate)
		c.JSON(http.StatusBadRequest, gin.H{
            "code": 400,
            "data": gin.H{
                "post_id": postID,
            },
            "message": "Post " + postID + " has already been liked by user",
        })
        return
    }

	stmt, err := db.Prepare("INSERT INTO LIKES(uid, post_id, date_liked) VALUES(?, ?, NOW())")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	defer stmt.Close()

	_, err = stmt.Exec(uid, postID)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
    var like Like
    var dateLikedStr string
    err = db.QueryRow("SELECT uid, post_id, date_liked FROM LIKES WHERE uid = ? AND post_id = ?", uid, postID).Scan(&like.UID, &like.PostID, &dateLikedStr)
    if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    like.DateLiked, err = time.Parse("2006-01-02 15:04:05", dateLikedStr)
    if err != nil {
        log.Println("Error parsing date:", err)
        return
    }

	c.JSON(http.StatusCreated, gin.H{
        "code": 201,
        "data": gin.H{
            "like": like,
        },
        "message": "Like created successfully",
    })
}

func deleteLike(c *gin.Context) {
	postID := c.Param("post_id")
	var data map[string]string
	if err := c.BindJSON(&data); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	uid := data["uid"]
    var existing Like
    var existingDate string
    err := db.QueryRow("SELECT uid, post_id, date_liked FROM LIKES WHERE uid = ? AND post_id = ?", uid, postID).Scan(&existing.UID, &existing.PostID, &existingDate)
    if err != nil {
        existing.DateLiked, err = time.Parse("2006-01-02 15:04:05", existingDate)
		c.JSON(http.StatusInternalServerError, gin.H{
            "code": 400,
            "message": "Post is not liked by user",
        })
        return
    }
	stmt, err := db.Prepare("DELETE FROM LIKES WHERE uid=? AND post_id=?")
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"message": "An error occurred deleting the like"})
		return
	}
	defer stmt.Close()

	result, err := stmt.Exec(uid, postID)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusInternalServerError, gin.H{"message": "An error occurred deleting the like"})
		return
	}

	rowsAffected, _ := result.RowsAffected()
	if rowsAffected == 0 {
		c.JSON(http.StatusBadRequest, gin.H{
            "code": 400,
            "message": "Post is not liked by user",
        })
		return
	}

	c.JSON(http.StatusOK, gin.H{
        "code": 204,
        "message": "Like deleted successfully",
    })
}
