# Guess The Word Java Backend

This is a Spring Boot implementation of the API backend. It currently provides
the root endpoint and registration/login endpoints compatible with the existing
frontend requests:

- `GET /`
- `POST /api/register?username=...&password=...&role=PLAYER`
- `POST /api/login?username=...&password=...`

## Run locally

Requirements: Java 17+ and Maven.

```bash
mvn spring-boot:run
```

The service runs on `http://127.0.0.1:8081`. It uses a local H2 database by
default. PostgreSQL can be selected with `SPRING_DATASOURCE_URL`,
`SPRING_DATASOURCE_USERNAME`, and `SPRING_DATASOURCE_PASSWORD`.

The original FastAPI backend remains available on port `8000`; switch the
frontend API URL to port `8081` when using this Java backend.