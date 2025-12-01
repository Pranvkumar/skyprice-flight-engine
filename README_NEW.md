# ✈️ SkyPrice - Premium Flight Search Engine

**Real-time flight price search with Amadeus API integration**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Amadeus](https://img.shields.io/badge/Amadeus-API-red)

## 🌟 Features

- ✈️ **Real-time Flight Data** from Amadeus API
- 🎨 **Premium UI** with Godly-inspired dark theme
- 🔍 **Smart Airport Search** with autocomplete
- 💰 **Live Price Comparison**
- 📊 **Price Statistics & Trends**
- 🚀 **Fast & Modern** FastAPI backend
- 📱 **Fully Responsive** design

## 🚀 Quick Start

```bash
cd Flight-Price-Engine/backend
python test_server.py
```

Open **http://localhost:8000**

## 📸 What You Get

- Premium dark UI with glassmorphism
- Real-time airport autocomplete
- Live flight prices from Amadeus
- Price statistics (lowest, highest, average)
- Modern animations and transitions

## 🔧 Tech Stack

**Backend:**
- Python 3.13
- FastAPI
- Amadeus SDK
- Uvicorn

**Frontend:**
- HTML5 + Modern CSS3
- Vanilla JavaScript
- Inter Font Family
- Glassmorphism Design

## 🌐 API Endpoints

```
GET  /                  - Premium UI
GET  /airports          - Search airports
GET  /flights           - Search flights  
GET  /health            - Health check
GET  /docs              - API documentation
```

## 📦 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on:
- ☁️ Render.com (FREE)
- 🚂 Railway.app
- ⚡ Vercel
- 📝 Replit
- 🐍 PythonAnywhere

## 🔑 Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Pranvkumar/coding.git
   cd coding/Flight-Price-Engine
   ```

2. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Add environment variables** (backend/.env):
   ```env
   AMADEUS_API_KEY=your_key
   AMADEUS_API_SECRET=your_secret
   AMADEUS_ENVIRONMENT=test
   ```

4. **Run server:**
   ```bash
   cd backend
   python test_server.py
   ```

## 💡 Usage Tips

- **Test Mode:** Try PAR (Paris) → LON (London) for guaranteed results
- **Production:** Change `AMADEUS_ENVIRONMENT=production` for full access
- **Free Tier:** 1,000 API calls/month with Amadeus

## 📚 Documentation

- [🚀 Deployment Guide](DEPLOYMENT.md)
- [🔧 Amadeus Setup](AMADEUS_SETUP.md)
- [🎨 UI Design Guide](UI_DESIGN_GUIDE.md)
- [✅ Success Report](AMADEUS_SUCCESS_REPORT.md)

## 🎊 Project Stats

- 🎨 **1,000+ lines** of premium UI
- 🔧 **2,360+ lines** of backend code
- ✨ **7 UI components** with glassmorphism
- 🌐 **6 REST API endpoints**
- 📚 **Complete documentation**

## 📱 Features Overview

### Airport Search
Type any city and get instant airport suggestions with:
- Airport name and IATA code
- City and country info
- Smart autocomplete

### Flight Search
Search flights between any airports:
- Real-time prices
- Multiple airlines
- Flight details (times, duration, class)
- Price statistics

### Premium UI
- Dark theme with gradient backgrounds
- Glassmorphic cards
- Smooth animations
- Responsive design
- Modern typography

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📄 License

MIT License

## 👤 Author

**Pranvkumar Kshirsagar**

- GitHub: [@Pranvkumar](https://github.com/Pranvkumar)
- Email: pranvkumar.kshirsagar@example.com

## 🌐 Links

- **Repository:** https://github.com/Pranvkumar/coding
- **Project:** Flight-Price-Engine
- **Live Demo:** Coming soon!

---

⭐ **Star this repo if you found it helpful!**

Made with ❤️ using Amadeus API
