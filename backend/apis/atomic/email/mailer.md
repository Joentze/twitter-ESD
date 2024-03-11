### RabbitMQ Message Format

The RabbitMQ publisher should send messages to the notification queue in a JSON format with the following structure:

```json
{
  "message_type": "<MessageEnum>",
  "email": "<Recipient Email>",
  "username": "<Recipient Username>"
}
```

- **`message_type` (string):** Specifies the type of message. It should be one of the following values defined in the `MessageEnum`:

  - `"WELCOME_EMAIL"`: Indicates a welcome email to be sent to a new user.
  - `"CONTENT_WARNING"`: Indicates a content removal warning email to be sent to a user.

- **`email` (string):** The email address of the recipient.

- **`username` (string):** The username of the recipient.

### Example Message Formats

#### Welcome Email Message:

```json
{
  "message_type": "WELCOME_EMAIL",
  "email": "example@example.com",
  "username": "example_user"
}
```

#### Content Removal Warning Email Message:

```json
{
  "message_type": "CONTENT_WARNING",
  "email": "example@example.com",
  "username": "example_user"
}
```

Ensure that the publisher sends messages adhering to this format for the microservice to correctly process and send emails based on the message type.
