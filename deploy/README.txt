1. To bootstrap dependencies:

   chmod +x start_services.sh
   ./start_services.sh

2. To run both backend and frontend together:

   chmod +x run_services.sh
   ./run_services.sh

3. To initialize GitHub remote and push:

   chmod +x init_github.sh
   ./init_github.sh

4. To deploy as systemd services:

   sudo cp agentic-backend.service /etc/systemd/system/
   sudo cp agentic-frontend.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now agentic-backend.service
   sudo systemctl enable --now agentic-frontend.service

5. To use the nginx config, copy deploy/nginx.conf into your Nginx sites-available and enable it.
