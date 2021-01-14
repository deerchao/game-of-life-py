rmdir /s /q dist\ui
robocopy src\ui dist\ui /e /is

rmdir /s /q dist\api
robocopy src\api dist\api /e /is /xd __pycache__
