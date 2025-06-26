# 🚀 Railway Distance Calculator - Deployment Guide

## Free Deployment Options with Custom Domain

### 1. **Streamlit Community Cloud** (Recommended - Easiest)

#### Step 1: Deploy to Streamlit Cloud
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `Vishalp1726/railway-distance-calculator`
5. Main file path: `complete_api_railway_calculator.py`
6. Click "Deploy!"

#### Step 2: Get Free Subdomain
Your app will be available at:
`https://vishalp1726-railway-distance-calculator-complete-api-ra-xyz123.streamlit.app`

#### Step 3: Custom Domain (Optional)
- **Free Domain Options:**
  - `.tk` domains from [Freenom](https://freenom.com)
  - `.ml`, `.ga`, `.cf` domains
  - GitHub student pack domains
- **Setup:** Configure CNAME record pointing to your Streamlit URL

---

### 2. **Render.com** (Alternative - Good Performance)

#### Step 1: Create Account
1. Visit [render.com](https://render.com)
2. Sign up with GitHub

#### Step 2: Deploy
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run complete_api_railway_calculator.py --server.port $PORT --server.address 0.0.0.0`
   - **Environment:** Python 3

#### Step 3: Custom Domain
- Free subdomain: `yourapp.onrender.com`
- Custom domain supported in free tier

---

### 3. **Railway.app** (Alternative - Developer Friendly)

#### Step 1: Setup
1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"

#### Step 2: Configure
```bash
# railway.json (create this file)
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run complete_api_railway_calculator.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"
  }
}
```

---

## 🔧 Pre-Deployment Checklist

### Required Files (Already Created)
- ✅ `requirements.txt` - Dependencies
- ✅ `streamlit_config.toml` - Streamlit configuration
- ✅ `secrets.toml` - Secrets template
- ✅ `complete_api_railway_calculator.py` - Main app

### Environment Variables
- `PORT` - Automatically set by platforms
- `RAPIDAPI_KEY` - Optional, for enhanced station search

---

## 🌐 Free Domain Options

### 1. **Freenom** (Free .tk, .ml, .ga, .cf domains)
- Visit [freenom.com](https://freenom.com)
- Register free domain
- Configure DNS to point to your app

### 2. **GitHub Student Pack**
- Free `.me` domain for students
- Visit [education.github.com](https://education.github.com)

### 3. **Free Subdomains**
- Most platforms provide free subdomains
- Example: `railway-calc.onrender.com`

---

## 📱 Mobile-Friendly Features

Your app is already optimized with:
- ✅ Responsive layout (`layout="wide"`)
- ✅ Mobile-friendly UI components
- ✅ Touch-friendly buttons and inputs
- ✅ Streamlit's built-in mobile support

---

## 🔐 Security Considerations

### For Production Deployment:
1. **Move API Keys to Secrets:**
   ```python
   google_api_key = st.secrets.get("google_api_key", "fallback_key")
   ```

2. **Environment Variables:**
   - Set `GOOGLE_MAPS_API_KEY` in platform secrets
   - Set `RAPIDAPI_KEY` if using RapidAPI

3. **Rate Limiting:**
   - Already implemented in the app
   - Monitor API usage

---

## 🚀 Quick Deploy Commands

### For Streamlit Cloud:
```bash
# Just push to GitHub and deploy via web interface
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### For Render/Railway:
```bash
# Add deployment config files
git add streamlit_config.toml railway.json
git commit -m "Add deployment configs"
git push origin main
```

---

## 📊 Expected Performance

### Free Tier Limitations:
- **Streamlit Cloud:** 1GB RAM, community support
- **Render:** 512MB RAM, sleeps after 15min inactivity
- **Railway:** 512MB RAM, $5 free credit monthly

### App Performance:
- ✅ Fast loading with cached station data
- ✅ Efficient Google Maps API usage
- ✅ Optimized for low resource usage

---

## 🎯 Recommended Deployment Flow

1. **Start with Streamlit Cloud** (easiest setup)
2. **Get free .tk domain** from Freenom
3. **Monitor usage** and upgrade if needed
4. **Consider Railway/Render** for better performance

Your Railway Distance Calculator will be accessible worldwide! 🌍 