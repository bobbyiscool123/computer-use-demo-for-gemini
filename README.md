<div align="center">
  <img src="https://storage.googleapis.com/generativeai-downloads/gemini_logo.png" alt="Gemini Logo" width="150"/>
  <h1>Gemini Computer Use Demo</h1>
</div>

<br>

**Welcome to the Gemini Computer Use Demo!**

This repository provides a starting point for experimenting with the computer use feature on Gemini. Below you'll find everything you need to get up and running with virtual environments, agent loops, compatible tools, and a Streamlit interface.

<br>

> [!CAUTION]
> **Important:** This code is provided as-is and has not been thoroughly tested. It may not function as intended and may contain errors. Use it at your own risk.
>
> Computer use is a beta feature. Please be aware that it poses unique risks, especially when interacting with the internet. Take the following precautions to minimize those risks:
>
> 1.  Use a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents.
> 2.  Avoid giving the model access to sensitive data, such as account login information, to prevent information theft.
> 3.  Limit internet access to an allowlist of domains to reduce exposure to malicious content.
> 4.  Ask a human to confirm decisions that may result in meaningful real-world consequences as well as any tasks requiring affirmative consent, such as accepting cookies, executing financial transactions, or agreeing to terms of service.
>
> In some circumstances, Gemini will follow commands found in content even if it conflicts with the user's instructions. For example, instructions on webpages or contained in images may override user instructions or cause Gemini to make mistakes. We suggest taking precautions to isolate Gemini from sensitive data and actions to avoid risks related to prompt injection.
>
> Please inform end users of relevant risks and obtain their consent prior to enabling computer use in your own products.

<br>

**Key features of this demo:**

*   Build files for creating a virtual environment with all dependencies.
*   A Gemini API agent loop for accessing the Gemini model.
*   Gemini-compatible computer use tools.
*   A Streamlit app for interacting with the agent loop.

<br>

**Share Your Feedback!**

We encourage you to provide feedback on the model responses, the API itself, or the documentation using [this form](https://forms.gle/BT1hpBrqDPDUrCqo7).

<br>

> [!IMPORTANT]
> The Beta API used in this reference implementation is subject to change. Please refer to the [API release notes](https://ai.google.dev/gemini/release-notes) for the most up-to-date information.
>
> Also note that the components are weakly separated: the agent loop runs in the virtual environment being controlled by Gemini, can only be used by one session at a time, and must be restarted or reset between sessions if necessary.

<br>

## Quickstart: Running the Application

### Gemini API Key
> [!TIP]
> You can find your API key in the [Google AI Studio](https://makersuite.google.com/app/apikey).
<br>

1.  **Set Environment Variables:** Before running, make sure to set the following environment variables in your Windows environment:
    *   `WIDTH`: Desired width of the virtual display (e.g., `1024`).
    *   `HEIGHT`: Desired height of the virtual display (e.g., `768`).
    *   `DISPLAY_NUM`: The display number to run the virtual display on (e.g., `1`).
    *   `GEMINI_API_KEY`: Your Google Gemini API Key. You will also need to set this in the Streamlit app's user interface.

2.  **Run the application:**
    *   Open a WSL terminal.
    *   Navigate to the project directory.
    *   Run `call setup.bat`.
    *   Then run `call entrypoint.bat`.
        ```batch
        call setup.bat
        call entrypoint.bat
        ```

3.  **Access the Demo App:** Once the application is running, open your browser to [http://localhost:8080](http://localhost:8080) to access the combined interface that includes both the agent chat and desktop view.

The application stores settings like the API key and custom system prompt in `~/.anthropic/`.

**Alternative access points:**

*   Streamlit interface only: [http://localhost:8501](http://localhost:8501)
*   Desktop view only: [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html)

<br>

## Screen Size

Environment variables `WIDTH` and `HEIGHT` control the screen size. We recommend using XGA/WXGA (1024x768) to avoid potential issues related to image resizing.

**Screen Size Guidelines:**

*   **Higher Resolutions:** Scale the image down to XGA, let the model interact with the scaled version, and then map the coordinates back to the original resolution proportionally.
*   **Lower Resolutions or Smaller Devices:** Add black padding around the display area until it reaches 1024x768.

<br>

## Development

1.  **Setup:** Ensure you have the following installed:
    *   Python 3.12 or lower
    *   Rust/Cargo
    *   Git
    *   Windows Subsystem for Linux
    *   NoVNC (Installed to `/opt/noVNC`)
2.  **Environment Variables:** Set the environment variables as described in the "Quickstart" section.
3.  **Navigate to the project directory:** Open your WSL terminal and navigate to the root of the `gemini-computer-use-demo` project directory.
4.  **Run Setup:** Run `setup.bat` to create a virtual environment and install dependencies.
    ```batch
       call setup.bat
    ```
5.  **Run the application:**
    ```batch
    call entrypoint.bat
    ```

The application will start a web server and launch the Streamlit app. The application can be viewed at [http://localhost:8080](http://localhost:8080).

The application uses a virtual environment. Make sure that the correct environment is active for development.

The application uses `pre-commit` hooks. If there are any errors during commit, you can use the command `pre-commit run --all-files` to run all pre-commit hooks.

<br>

**Model Recommendation:**

This demo is optimized for the `gemini-2.0-flash-exp` model. Please ensure you are using this model or a compatible one for the best performance.

<br>

> [!IMPORTANT]
> The Beta API used in this reference implementation is subject to change. Please refer to the API release notes for the most up-to-date information.