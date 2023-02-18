from enum import Enum

from django.conf import settings
from django.contrib.auth.decorators import login_required

class BaseEnum(Enum):
    @classmethod
    def keys(cls):
        return [k.name for k in cls]

    @classmethod
    def values(cls):
        return [k.value for k in cls]

    @classmethod
    def items(cls):
        return [(k.value, k.name) for k in cls]


class ProgressChoiceEnum(BaseEnum): 
    PENDING = "En attente"
    IN_PROGESS = "en cours"
    CANCELLED = "Annulé"
    COMPLETED = "Terminé"
  
 
    
class TypeVoterEnum(BaseEnum): 
    CANDIDATE = "CANDIDAT"
    CITIZEN = "CITOYEN"
    

class TypeElectionEnum(BaseEnum): 
    PRIVATE = "PRIVEE"
    PUBLIC = "PUBLIQUE"
    
    
class NotificationTypeEnum(BaseEnum):
    NEW_VOTE = "Création d'un vote"
    RAPPEL = "Rapplel d'un vote en cours"
    ELLECTION_RESUSLT = "Résultat d'une élection"
    ADMIN_REQUEST = "Demande de droits d'Admin de vote"



    
       
    
   


    