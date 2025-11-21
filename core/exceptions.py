class ApplicationError(Exception):
    """Base pour toutes les erreurs métier."""
    pass


class NotFoundError(ApplicationError):
    """Ressource non trouvée."""
    pass


class ConflictError(ApplicationError):
    """Conflit de données (ex: doublon unique)."""
    pass


class ValidationError(ApplicationError):
    """Erreur de validation métier (différente de la validation Pydantic)."""
    pass


class UnauthorizedError(ApplicationError):
    """Accès refusé (non authentifié ou non autorisé)."""
    pass
