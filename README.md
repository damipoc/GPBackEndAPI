# GPBackEndAPI

Backend API endpoint for receiving, validating and forwarding data received from the hardware.

Creates an exposed endpoint to allow the wifi connected hardware to POST json data there.  
The endpoint is `/devices/<device>/telemetry` with `<devices>` being the device ID.  
The expected data format will be validated and reconstructed into a dictionary and sent
to the database.
  
`backendapi.py` is the finalised version to be part of the whole project.  
`api.py` is for testing purposes and can be used alone without being part of the whole project for testing purposes.
