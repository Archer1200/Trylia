# Frontend - Your Virtual Dressing Room

A simple, minimal e-commerce website built with React featuring a clean design and responsive layout.

## Features

- **Home Page**: Hero section with website branding and call-to-action
- **Catalog Page**: Product grid with 3 shirt items from local images
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Clean UI**: Minimal design with custom CSS (no frameworks)
- **Navigation**: Simple routing between pages

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- npm or yarn package manager

### Installation

1. Navigate to the project directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and visit `http://localhost:3000`

### Building for Production

To create a production build:

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   └── ProductCard.js
│   ├── pages/
│   │   ├── Home.js
│   │   └── Catalog.js
│   ├── styles/
│   │   ├── App.css
│   │   ├── Header.css
│   │   ├── Home.css
│   │   ├── Catalog.css
│   │   └── ProductCard.css
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

## Technologies Used

- React 18
- React Router DOM
- Custom CSS (no external UI frameworks)
- Google Fonts (Inter)

## Features Overview

### Home Page
- Hero section with gradient background
- Website title "Frontend" and tagline "Your Virtual Dressing Room"
- Call-to-action button linking to catalog
- Features section highlighting key benefits

### Catalog Page
- Grid layout displaying 3 shirts
- Product cards with local shirt images, names, prices, and categories
- Hover effects and interactive elements
- "Try On" buttons (visual only, no backend functionality)

### Design Principles
- Clean and minimal aesthetic
- Consistent color scheme
- Responsive grid layouts
- Smooth animations and transitions
- Accessible design with proper focus states

## Customization

You can easily customize the website by:

1. **Colors**: Update the CSS custom properties in the style files
2. **Products**: Modify the shirt data in `src/pages/Catalog.js` or add more shirt images to `public/images/shirts/`
3. **Content**: Edit text content in the component files
4. **Styling**: Adjust the CSS files for different visual preferences

## Browser Support

This website supports all modern browsers including:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available under the MIT License.