# DataPulse Test Frontend

Simple HTML frontend to test the DataPulse API.

## Quick Start

1. **Open the frontend:**
   ```bash
   # Open in browser
   start frontend/index.html
   ```

2. **Login:**
   - Email: `ashertettehabotsi@gmail.com`
   - Password: `asherasher1!`
   - Click "Login"

3. **Upload a dataset:**
   - Enter a dataset name
   - Choose `sample.csv` (provided) or your own CSV/JSON file
   - Click "Upload"

4. **View datasets:**
   - Click "Refresh List" to see uploaded datasets

## Features

- ✅ JWT Authentication
- ✅ File Upload (CSV/JSON)
- ✅ Dataset List View
- ✅ Clean, minimal UI

## API Endpoints Used

- `POST /api/auth/login` - Login
- `POST /api/datasets/upload/` - Upload dataset
- `GET /api/datasets/` - List datasets

## Notes

- Make sure backend is running on `http://localhost:8000`
- CORS must be enabled in Django settings
- Sample CSV file included for testing
