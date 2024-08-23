# Hospital Management API Collection

## Setup and Deployment

### 1. Deploy Flask App using Docker Compose

Untuk mendeploy aplikasi Flask yang terhubung dengan database PostgreSQL eksternal, gunakan Docker Compose dengan langkah-langkah berikut:

1. **Jalankan Docker Compose**:

    ```bash
    docker-compose up --build
    ```

    Perintah ini akan membangun image dari Dockerfile dan memulai container untuk Flask App.

3. **Akses aplikasi** di browser Anda di `http://localhost:5000`.

## Environment Variables

- `DATABASE_URL`: URL database eksternal Anda

## Requirements

- Docker
- Docker Compose

## Authors

- [Ulul 'Azmi Abdullah Iman](https://github.com/azmiman52)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
