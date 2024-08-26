
# FlowForge Application Documentation

## Overview

FlowForge is a modular desktop application designed to manage various plugins, both functional and UI-based. The application is built using Python and PyQt5, providing a modern, customizable UI for different workflows.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Application Structure](#application-structure)
3. [UI Plugins](#ui-plugins)
4. [Function Plugins](#function-plugins)
5. [Event Handling](#event-handling)
6. [Session Management](#session-management)
7. [Adding New Plugins](#adding-new-plugins)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

- Python 3.8+
- PyQt5
- Watchdog (for file monitoring)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/flowforge.git
    cd flowforge
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv .flowforge_env
    source .flowforge_env/bin/activate  # On Windows use: .flowforge_env\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python main.py
    ```

## Application Structure

The application is organized into several core components:

- **main.py**: Entry point of the application.
- **core/**: Contains essential modules like plugin management, logging, and event handling.
- **modules/**: Directory where all plugins (both UI and function-based) are stored.
- **ui/**: Contains UI-related components like `MainWindow`.

## UI Plugins

UI Plugins are responsible for adding interactive components to the application's UI.

### Example: `ExampleUiPlugin`

```python
class ExampleUiPlugin(UIPluginBase):
    def on_initialize(self, layout=None, main_window=None, *args, **kwargs):
        # Initialization logic for the UI Plugin
```

### Adding a UI Plugin

1. Create a new directory in `modules/` for your plugin.
2. Implement the plugin by subclassing `UIPluginBase`.
3. Add the necessary UI components in the `on_initialize` method.

## Function Plugins

Function Plugins are non-UI components that provide additional functionality to the application.

### Example: `PathMonitor`

```python
class PathMonitor(FunctionPluginBase):
    def on_initialize(self):
        # Initialization logic for the function plugin
```

### Adding a Function Plugin

1. Create a new directory in `modules/` for your plugin.
2. Implement the plugin by subclassing `FunctionPluginBase`.
3. Add the necessary logic in the `on_initialize` method.

## Event Handling

The application uses an event bus system to facilitate communication between different components.

### Registering for an Event

```python
event_bus.register("event_name", self.event_handler)
```

### Posting an Event

```python
event_bus.post("event_name", *args, **kwargs)
```

## Session Management

The application supports saving and restoring the session layout.

### Saving the Session

The session is automatically saved when the application is closed.

### Restoring the Session

The session is restored on application startup, allowing the user to continue where they left off.

## Adding New Plugins

To add a new plugin:

1. Create a new directory under `modules/`.
2. Implement the plugin by subclassing `UIPluginBase` or `FunctionPluginBase`.
3. Ensure the plugin is correctly initialized by the `PluginManager`.

## Troubleshooting

- **Issue**: Plugin not loading.
    - **Solution**: Ensure the plugin class is correctly subclassed and located in the `modules/` directory.

- **Issue**: UI components not displaying correctly.
    - **Solution**: Check the `on_initialize` method in your UI plugin to ensure all components are correctly initialized and added to the main window.

## Contact

For further assistance, please contact the developer team at `support@flowforge.com`.

---

This documentation provides an overview of the FlowForge application and instructions on how to use and extend it. For more detailed information, please refer to the source code and comments within the application.
