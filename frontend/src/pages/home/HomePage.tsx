import LoginButton from "../../components/auth/LoginButton";
import YapperIconLarge from "../../misc/YapperIconLarge";

const HomePage = () => {
  return (
    <div className="hero min-h-screen bg-gradient-to-br from-slate-50 via-slate-100 to-violet-600">
      <div className="hero-content flex-col lg:flex-row gap-32">
        <div className="flex flex-row gap-8">
          <YapperIconLarge />
          <p className="m-auto text-6xl font-bold text-primary">.com</p>
        </div>
        <div>
          <h1 className="text-5xl font-bold text-primary">
            Meet The New Twitter...
          </h1>
          <p className="py-6 max-w-96">
            "Introducing Yapper - where freedom of expression meets peace of
            mind. With our enhanced content safety features, be a hero of
            positivity and connect fearlessly. Join Yapper today and elevate
            your voice responsibly."
          </p>
          <LoginButton />
        </div>
      </div>
    </div>
  );
};
export default HomePage;
