

# Appointment Scheduling System - Desktop Application

A robust cross-platform desktop client built with **Electron**, designed to seamlessly wrap and deliver the **Next.js** web application experience with native system integration.

## 🚀 Key Features

* **Native Wrapper**: Complete packaging of the Next.js web interface.
* **Cross-Platform**: Full support for Windows, macOS, and Linux.
* **System Integration**: Native OS menus and global keyboard shortcuts.
* **Security**: Implementation of secure context via `preload.js`.
* **Persistence**: Shared local storage and session handling consistent with the web browser.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

* **Node.js**: Version 18.0 or higher.
* **Package Manager**: `npm` or `yarn`.
* **Web Instance**: The Next.js web application must be either running (development) or built (production).

## 🛠️ Installation

1. **Clone the repository and navigate to the desktop directory:**
```bash
cd Frontend/apps/desktop

```


2. **Install dependencies:**
```bash
npm install

```



## ▶️ Running the Application

### Development Mode

To work with Hot Module Replacement (HMR):

1. **Start the Web App (Terminal 1):**
```bash
cd ../web
npm run dev

```


2. **Launch Electron (Terminal 2):**
```bash
cd ../desktop
npm run dev

```



*The app will automatically point to `http://localhost:3000*`.

### Production Mode

1. **Build the Web App:**
```bash
cd ../web
npm run build

```


2. **Launch the Desktop Environment:**
```bash
cd ../desktop
npm run start

```



## 📦 Packaging & Distribution

Generate production-ready executables located in the `dist/` folder.

| Platform | Command |
| --- | --- |
| **Windows** | `npm run build:win` |
| **macOS** | `npm run build:mac` |
| **Linux** | `npm run build:linux` |

## 📁 Project Structure

```text
desktop/
├── main.js          # Electron main process (entry point)
├── preload.js       # Secure bridge between Electron and Web
├── package.json     # Scripts, dependencies, and build config
├── assets/          # Application icons and static branding
└── dist/            # Compiled binaries (generated after build)

```

## ⚙️ Customization

* **App Branding**: Update `productName` in `package.json` within the `build` configuration.
* **Icons**: Replace the files in `assets/` using the following formats:
* `icon.ico` (Windows)
* `icon.icns` (macOS)
* `icon.png` (Linux)



## 🐛 Troubleshooting

* **White Screen / App not loading**:
* Ensure the web server is active at the expected port (3000 by default).
* Verify the Next.js build folder exists if running in production mode.


* **CORS Policy Errors**:
* The backend/web API must whitelist the Electron origin (or `file://` protocol if using static assets).



