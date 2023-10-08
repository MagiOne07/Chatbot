inute ago in 2m 51s
Search logs
3s
3s
2m 44s
[16:02:38+0000] Collecting tensorflow==2.8.0
"2023-10-08 16:04:16"|ERROR|[16:02:37+0000] Collecting streamlit==1.9.0
[16:02:37+0000]   Using cached streamlit-1.9.0-py2.py3-none-any.whl (10.1 MB)
[16:02:37+0000] Collecting streamlit-chat==0.0.2.1
[16:02:37+0000]   Using cached streamlit_chat-0.0.2.1-py3-none-any.whl (1.2 MB)
[16:02:37+0000] Collecting streamlit-option-menu==0.3.2
[16:02:37+0000]   Using cached streamlit_option_menu-0.3.2-py3-none-any.whl (712 kB)
[16:02:38+0000] Collecting tensorflow==2.8.0 | Exit code: 137 | Please review your requirements.txt | More information: https://aka.ms/troubleshoot-python
\n/bin/bash -c "oryx build /tmp/zipdeploy/extracted -o /home/site/wwwroot --platform python --platform-version 3.8 -p virtualenv_name=antenv --log-file /tmp/build-debug.log  -i /tmp/8dbc817e72c7971 --compress-destination-dir | tee /tmp/oryx-build.log ; exit $PIPESTATUS "

Generating summary of Oryx build
Parsing the build logs
Found 1 issue(s)

Build Summary :
===============
Errors (1)
1. [16:02:37+0000] Collecting streamlit==1.9.0\n[16:02:37+0000]   Using cached streamlit-1.9.0-py2.py3-none-any.whl (10.1 MB)\n[16:02:37+0000] Collecting streamlit-chat==0.0.2.1\n[16:02:37+0000]   Using cached streamlit_chat-0.0.2.1-py3-none-any.whl (1.2 MB)\n[16:02:37+0000] Collecting streamlit-option-menu==0.3.2\n[16:02:37+0000]   Using cached streamlit_option_menu-0.3.2-py3-none-any.whl (712 kB)\n[16:02:38+0000] Collecting tensorflow==2.8.0  
-  Next Steps: Please review your requirements.txt
-  For more details you can browse to https://aka.ms/troubleshoot-python

Warnings (0)

Deployment Failed. deployer = GITHUB_ZIP_DEPLOY deploymentPath = ZipDeploy. Extract zip. Remote build.
Error: Failed to deploy web package to App Service.
Error: Deployment Failed, Package deployment using ZIP Deploy failed. Refer logs for more details.
App Service Application URL: https://othstchatbot.azurewebsites.net
