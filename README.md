# Gemini Computer Use Demo

> [!CAUTION]
> **This code is provided as-is and has not been thoroughly tested. It may not work as expected and may contain errors. Use at your own risk.**
>
> Computer use is a beta feature. Please be aware that computer use poses unique risks that are distinct from standard API features or chat interfaces. These risks are heightened when using computer use to interact with the internet. To minimize risks, consider taking precautions such as:
>
> 1. Use a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents.
> 2. Avoid giving the model access to sensitive data, such as account login information, to prevent information theft.
> 3. Limit internet access to an allowlist of domains to reduce exposure to malicious content.
> 4. Ask a human to confirm decisions that may result in meaningful real-world consequences as well as any tasks requiring affirmative consent, such as accepting cookies, executing financial transactions, or agreeing to terms of service.
>
> In some circumstances, Gemini will follow commands found in content even if it conflicts with the user's instructions. For example, instructions on webpages or contained in images may override user instructions or cause Gemini to make mistakes. We suggest taking precautions to isolate Gemini from sensitive data and actions to avoid risks related to prompt injection.
>
> Finally, please inform end users of relevant risks and obtain their consent prior to enabling computer use in your own products.

This repository helps you get started with computer use on Gemini, with reference implementations of:

*   Build files to create a virtual environment with all necessary dependencies.
*   A computer use agent loop using the Gemini API to access the Gemini model.
*   Gemini-compatible computer use tools.
*   A Streamlit app for interacting with the agent loop.

Please use [this form](https://forms.gle/BT1hpBrqDPDUrCqo7) to provide feedback on the quality of the model responses, the API itself, or the quality of the documentation - we cannot wait to hear from you!

> [!IMPORTANT]
> The Beta API used in this reference implementation is subject to change. Please refer to the [API release notes](https://cloud.google.com/vertex-ai/docs/gemini/release-notes) for the most up-to-date information.

> [!IMPORTANT]
> The components are weakly separated: the agent loop runs in the virtual environment being controlled by Gemini, can only be used by one session at a time, and must be restarted or reset between sessions if necessary.

## Quickstart: running the application

### Gemini API

> [!TIP]
> You can find your API key in the [Google Cloud Console](https://console.cloud.google.com/).

1.  **Set Environment Variables:** Ensure you have the following environment variables set in your Windows environment before running:
    *   `WIDTH`: Desired width of the virtual display (e.g., `1024`).
    *   `HEIGHT`: Desired height of the virtual display (e.g., `768`).
    *   `DISPLAY_NUM`: The display number to run the virtual display on (e.g., `1`).
    *   `GEMINI_API_KEY`: Your Google Gemini API Key. You will also have to set this in the streamlit app in the user interface.

2.  **Run the application:**
     * Open a WSL terminal
     * Navigate to the project directory
     * Run `call setup.bat`
     * Then run `call entrypoint.bat`
        ```batch
        call setup.bat
        call entrypoint.bat
        ```

3.  **Access the Demo App:** Once the application is running, open your browser to [http://localhost:8080](http://localhost:8080) to access the combined interface that includes both the agent chat and desktop view.

The application stores settings like the API key and custom system prompt in `~/.anthropic/`.

Alternative access points:

-   Streamlit interface only: [http://localhost:8501](http://localhost:8501)
-   Desktop view only: [http://localhost:6080/vnc.html](http://localhost:6080/vnc.html)

## Screen size

Environment variables `WIDTH` and `HEIGHT` are used to set the screen size. We do not recommend sending screenshots in resolutions above [XGA/WXGA](https://en.wikipedia.org/wiki/Display_resolution_standards#XGA) to avoid issues related to image resizing.

When implementing computer use yourself, we recommend using XGA resolution (1024x768):

*   For higher resolutions: Scale the image down to XGA and let the model interact with this scaled version, then map the coordinates back to the original resolution proportionally.
*   For lower resolutions or smaller devices (e.g., mobile devices): Add black padding around the display area until it reaches 1024x768.

## Development

1.  **Setup:** Make sure you have the following installed:
    *   Python 3.12 or lower
    *   Rust/Cargo
    *   Git
    *   Windows Subsystem for Linux
    *   NoVNC (Installed to `/opt/noVNC`)
2.  **Environment Variables:** Set the environment variables as described in the "Quickstart" section.
3.  **Navigate to the project directory:** Open your WSL terminal and navigate to the root of the `gemini-computer-use-demo` project directory.
4. **Run Setup:** Run `setup.bat` to create a virtual environment and install dependencies.
    ```batch
       call setup.bat
    ```
5.  **Run the application:**
    ```batch
    call entrypoint.bat
    ```

The application will start up a web server and launch the streamlit app. The application can be viewed at [http://localhost:8080](http://localhost:8080).

The application uses a virtual environment. Make sure that the correct environment is active for development.

The application uses `pre-commit` hooks. If there are any errors during commit, you can use the command `pre-commit run --all-files` to run all pre-commit hooks.

**Model Recommendation:**

This demo is optimized for the `gemini-2.0-flash-exp` model. Please ensure you are using this model or a compatible one for the best performance.