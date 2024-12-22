# Gemini Computer Use Demo

> [!CAUTION]
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

* Build files to create a Docker container with all necessary dependencies
* A computer use agent loop using the Gemini API to access the Gemini model
* Gemini-defined computer use tools
* A streamlit app for interacting with the agent loop

Please use [this form](https://forms.gle/BT1hpBrqDPDUrCqo7) to provide feedback on the quality of the model responses, the API itself, or the quality of the documentation - we cannot wait to hear from you!

> [!IMPORTANT]
> The Beta API used in this reference implementation is subject to change. Please refer to the [API release notes](https://cloud.google.com/vertex-ai/docs/gemini/release-notes) for the most up-to-date information.

> [!IMPORTANT]
> The components are weakly separated: the agent loop runs in the container being controlled by Gemini, can only be used by one session at a time, and must be restarted or reset between sessions if necessary.

## Quickstart: running the Docker container

### Gemini API

> [!TIP]
> You can find your API key in the [Google Cloud Console](https://console.cloud.google.com/).

You'll need to pass in Google Cloud credentials with appropriate permissions to use Gemini.

```bash
docker build . -t gemini-computer-use-demo
gcloud auth application-default login
export VERTEX_REGION=%your_vertex_region%
export VERTEX_PROJECT_ID=%your_vertex_project_id%
docker run \
    -e API_PROVIDER=vertex \
    -e CLOUD_ML_REGION=$VERTEX_REGION \
    -e GEMINI_VERTEX_PROJECT_ID=$VERTEX_PROJECT_ID \
    -v $HOME/.config/gcloud/application_default_credentials.json:/home/computeruse/.config/gcloud/application_default_credentials.json \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -it gemini-computer-use-demo