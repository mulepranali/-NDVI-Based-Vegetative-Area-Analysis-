# 🌱 Vegetation Analysis Web Application

A comprehensive web-based vegetation monitoring system that analyzes satellite imagery using NDVI (Normalized Difference Vegetation Index) calculations. Built with Python Flask and modern web technologies for environmental monitoring and agricultural analysis.

## 🚀 Features

- **Satellite Image Processing**: Upload and analyze B04 (Red) and B08 (NIR) satellite bands
- **NDVI Calculation**: Real-time vegetation index computation
- **Vegetation Classification**: Automatic classification into healthy, moderate, and unhealthy zones
- **Interactive Visualization**: Color-coded maps with contour overlays
- **PDF Report Generation**: Comprehensive reports with statistics and visualizations
- **Multiple Export Options**: View, download images, and generate PDF reports
- **Responsive Design**: Modern UI that works on desktop and mobile devices

## 🛠️ Technologies Used

- **Backend**: Python, Flask, NumPy, OpenCV, Rasterio, ReportLab
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Processing**: NDVI calculations, geospatial analysis
- **Visualization**: Matplotlib, interactive charts
- **Documentation**: PDF generation with professional formatting

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd MHRSC
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
Ensure all required packages are installed:
- Flask
- NumPy
- OpenCV (opencv-python)
- Rasterio
- Matplotlib
- ReportLab

## 🏃‍♂️ Running the Application

### Method 1: Using Python Directly
```bash
python backend.py
```

### Method 2: Using Flask CLI
```bash
export FLASK_APP=backend.py
export FLASK_ENV=development
flask run
```

### Method 3: Windows PowerShell
```powershell
python backend.py
```

## 🌐 Accessing the Application

Once the server is running, open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 📱 Available Pages

- **Home** (`/`): Landing page with project overview
- **About** (`/about`): Detailed project information and methodology
- **Visualize** (`/visualize`): Main analysis interface

## 📊 How to Use

### 1. Upload Satellite Data
- Navigate to the Visualize page
- Upload B04 (Red band) satellite image (.tif/.tiff format)
- Upload B08 (NIR band) satellite image (.tif/.tiff format)

### 2. Analyze Vegetation
- Click "Analyze" to process the images
- View real-time NDVI calculation results
- See vegetation health statistics

### 3. Export Results
- **View Image**: Open processed image in new tab
- **Download Image**: Save NDVI visualization
- **Download Report PDF**: Generate comprehensive analysis report

## 📁 Project Structure

```
MHRSC/
├── backend.py              # Main Flask application
├── ndvi_utils.py           # NDVI calculation utilities
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── home.html          # Landing page
│   ├── about.html         # About page
│   └── index.html         # Analysis interface
├── uploads/               # Uploaded satellite images
├── results/               # Generated NDVI images
├── reports/               # Generated PDF reports
└── static/                # Static assets (CSS, JS, images)
```

## 🔧 Configuration

### Environment Variables (Optional)
```bash
export FLASK_ENV=development  # For development mode
export FLASK_DEBUG=1          # Enable debug mode
```

### Custom Settings
- Modify upload file size limits in `backend.py`
- Adjust NDVI classification thresholds in `ndvi_utils.py`
- Customize PDF report styling in the download_report function

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill existing process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Permission Errors**
   ```bash
   # Ensure write permissions for uploads/results folders
   chmod 755 uploads results reports
   ```

4. **Rasterio Installation Issues**
   ```bash
   # On Windows, you might need:
   conda install -c conda-forge rasterio
   ```

## 📈 NDVI Analysis Details

The application calculates NDVI using the formula:
```
NDVI = (NIR - Red) / (NIR + Red)
```

**Vegetation Classification:**
- **Healthy**: NDVI > 0.5 (Green)
- **Moderate**: 0.2 ≤ NDVI ≤ 0.5 (Yellow)
- **Unhealthy**: NDVI < 0.2 (Red)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the code comments for implementation details

## 🔮 Future Enhancements

- Time-series analysis capabilities
- Additional vegetation indices (EVI, NDWI)
- Cloud-based processing
- Real-time satellite data integration
- Mobile application development

---

**Built with ❤️ for environmental monitoring and sustainable agriculture**
