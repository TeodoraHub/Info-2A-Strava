class Session:
    """Classe pour gérer la session utilisateur (Singleton)"""
    
    _instance = None
    
    def __new__(cls):
        """Implémentation du pattern Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user = None
        return cls._instance
    
    def get_user(self):
        """Retourne l'utilisateur connecté
        
        Returns
        -------
        Utilisateur or None
            L'utilisateur connecté, ou None si aucun utilisateur n'est connecté
        """
        return self.user
    
    def set_user(self, user):
        """Définit l'utilisateur connecté
        
        Parameters
        ----------
        user : Utilisateur
            L'utilisateur à connecter
        """
        self.user = user
    
    def clear(self):
        """Déconnecte l'utilisateur"""
        self.user = None
    
    def is_connected(self):
        """Vérifie si un utilisateur est connecté
        
        Returns
        -------
        bool
            True si un utilisateur est connecté, False sinon
        """
        return self.user is not None
    
    @classmethod
    def reset(cls):
        """Reset le singleton (utile pour les tests)"""
        cls._instance = None