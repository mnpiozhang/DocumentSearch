from celery.decorators import task  
from celery.utils.log import get_task_logger  
from models import DocumentInfo

logger = get_task_logger(__name__)  
 
@task(name="analyze_uploadfile_task")  
def analyze_uploadfile_task(id):
    DocumentInfoObj = DocumentInfo.objects.get(id=id)
    DocumentInfoObj.indexstate = 'i'
    DocumentInfoObj.save()
    return ['aaa']