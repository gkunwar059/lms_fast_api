from fastapi import Request
from logger import logger
import time
from starlette.responses import Response

async def log_middleware(request:Request,call_next):
    start=time.time()
 
    response=await call_next(request)
    
    process_time=time.time()-start
    log_dict={
        'url':request.url.path,
        'ip_address':request.client.host,
        'method':request.method,
        'status_code':response.status_code,
        'process_time':process_time
        
    }
    logger.info(f"Request recieved at {request.url}",extra=log_dict)
    
    return response
