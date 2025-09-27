"""Configuration module for the Enhanced Keyword Search Engine."""

# Extended query patterns for better matching
QUERY_PATTERNS = {
    # Registration & Account related
    'register': ['registration', 'signup', 'register', 'account', 'login', 'sign up', 'create account', 'new account'],
    'login': ['login', 'sign in', 'access account', 'log in', 'enter account'],
    'profile': ['profile', 'account settings', 'personal info', 'update info', 'edit profile', 'my account'],
    'password': ['password', 'reset password', 'forgot password', 'change password', 'recover password', 'lost password'],
    
    # Financial operations
    'deposit': ['deposit', 'add funds', 'top up', 'fund account', 'money in', 'put money', 'transfer in', 'send money'],
    'withdraw': ['withdraw', 'withdrawal', 'take out money', 'cash out', 'payout', 'transfer out', 'get money', 'receive money'],
    'balance': ['balance', 'wallet', 'account balance', 'funds', 'how much money', 'current balance', 'available funds'],
    'payment': ['payment', 'payment method', 'payment options', 'how to pay', 'pay by', 'payment gateway'],
    
    # Investment related
    'invest': ['invest', 'investment', 'buy shares', 'shares', 'companies', 'invest money', 'start investing'],
    'returns': ['returns', 'earnings', 'profit', 'roi', 'return on investment', 'how much earn', 'income', 'yield'],
    'plans': ['plans', 'investment plans', 'phases', 'packages', 'tiers', 'options', 'strategies'],
    'risk': ['risk', 'safe', 'security', 'guarantee', 'protected', 'secure', 'is it safe'],
    
    # Referral program
    'referral': ['referral', 'refer', 'invite friends', 'earn money', 'bonus', 'friend bonus', 'refer friend'],
    'commission': ['commission', 'earnings', 'referral bonus', 'how much', 'percentage', 'rate'],
    
    # Platform information
    'about': ['about', 'what is', 'overview', 'company', 'platform', 'tell me about', 'what does'],
    'how_it_works': ['how it works', 'how to', 'steps', 'process', 'guide', 'procedure', 'workflow'],
    'features': ['features', 'benefits', 'advantages', 'what can i do', 'capabilities', 'functions'],
    'statistics': ['statistics', 'stats', 'numbers', 'how many', 'data', 'figures', 'metrics'],
    
    # Support & Contact
    'support': ['support', 'help', 'contact', 'customer service', 'assistance', 'need help', 'get help'],
    'issues': ['problem', 'issue', 'not working', 'error', 'bug', 'broken', 'fix', 'trouble'],
    
    # User levels
    'levels': ['levels', 'tiers', 'upgrade', 'progress', 'user level', 'rank', 'status'],
    
    # Testimonials
    'testimonials': ['testimonials', 'reviews', 'feedback', 'what people say', 'user experiences', 'opinions'],
}

# Enhanced direct keyword to category/subcategory mapping
KEYWORD_MAPPING = {
    # Registration & Account
    'registration': ('Account Management', 'registration'),
    'signup': ('Account Management', 'registration'),
    'register': ('Account Management', 'registration'),
    'login': ('Account Management', 'registration'),
    'account': ('Account Management', 'registration'),
    'profile': ('Account Management', 'registration'),
    'password': ('Account Management', 'registration'),
    'create account': ('Account Management', 'registration'),
    'new account': ('Account Management', 'registration'),
    'log in': ('Account Management', 'registration'),
    'sign in': ('Account Management', 'registration'),
    'reset password': ('Account Management', 'registration'),
    'forgot password': ('Account Management', 'registration'),
    'change password': ('Account Management', 'registration'),
    
    # Financial operations
    'deposit': ('Financial Operations', 'deposit'),
    'deposits': ('Financial Operations', 'deposit'),
    'add funds': ('Financial Operations', 'deposit'),
    'top up': ('Financial Operations', 'deposit'),
    'fund': ('Financial Operations', 'deposit'),
    'payment': ('Financial Operations', 'deposit'),
    'payments': ('Financial Operations', 'deposit'),
    'transfer in': ('Financial Operations', 'deposit'),
    'send money': ('Financial Operations', 'deposit'),
    'withdraw': ('Financial Operations', 'withdrawal'),
    'withdrawal': ('Financial Operations', 'withdrawal'),
    'withdrawals': ('Financial Operations', 'withdrawal'),
    'payout': ('Financial Operations', 'withdrawal'),
    'cash out': ('Financial Operations', 'withdrawal'),
    'transfer out': ('Financial Operations', 'withdrawal'),
    'get money': ('Financial Operations', 'withdrawal'),
    'receive money': ('Financial Operations', 'withdrawal'),
    'balance': ('Financial Operations', 'wallet'),
    'wallet': ('Financial Operations', 'wallet'),
    'account balance': ('Financial Operations', 'wallet'),
    'available funds': ('Financial Operations', 'wallet'),
    
    # Investment related
    'invest': ('Investment', 'companies'),
    'investment': ('Investment', 'companies'),
    'investing': ('Investment', 'companies'),
    'shares': ('Investment', 'companies'),
    'companies': ('Investment', 'companies'),
    'returns': ('Investment', 'companies'),
    'earnings': ('Investment', 'companies'),
    'profit': ('Investment', 'companies'),
    'roi': ('Investment', 'companies'),
    'plans': ('Investment', 'companies'),
    'phases': ('Investment', 'companies'),
    'packages': ('Investment', 'companies'),
    'strategies': ('Investment', 'companies'),
    
    # Referral program
    'referral': ('Referral Program', 'referral'),
    'refer': ('Referral Program', 'referral'),
    'invite': ('Referral Program', 'referral'),
    'friends': ('Referral Program', 'referral'),
    'commission': ('Referral Program', 'referral'),
    'bonus': ('Bonuses', 'bonus'),
    'friend bonus': ('Referral Program', 'referral'),
    
    # Platform information
    'about': ('Platform Overview', 'about'),
    'overview': ('Platform Overview', 'about'),
    'platform': ('Platform Overview', 'about'),
    'company': ('Platform Overview', 'about'),
    'how': ('Platform Overview', 'how_it_works'),
    'works': ('Platform Overview', 'how_it_works'),
    'steps': ('Platform Overview', 'how_it_works'),
    'process': ('Platform Overview', 'how_it_works'),
    'features': ('Platform Overview', 'features'),
    'benefits': ('Platform Overview', 'features'),
    'statistics': ('Platform Overview', 'stats'),
    'stats': ('Platform Overview', 'stats'),
    'numbers': ('Platform Overview', 'stats'),
    'metrics': ('Platform Overview', 'stats'),
    
    # Support & Contact
    'support': ('Contact & Support', 'contact'),
    'contact': ('Contact & Support', 'contact'),
    'help': ('Contact & Support', 'contact'),
    'customer service': ('Contact & Support', 'contact'),
    'assistance': ('Contact & Support', 'contact'),
    
    # User levels
    'levels': ('Account Management', 'levels'),
    'tiers': ('Account Management', 'levels'),
    'upgrade': ('Account Management', 'levels'),
    'rank': ('Account Management', 'levels'),
    'status': ('Account Management', 'levels'),
    
    # Testimonials
    'testimonials': ('User Reviews', 'testimonials'),
    'reviews': ('User Reviews', 'testimonials'),
    'feedback': ('User Reviews', 'testimonials'),
}

# Synonyms and alternative phrasings
SYNONYMS = {
    'register': ['signup', 'create account', 'make account'],
    'login': ['sign in', 'log in', 'enter'],
    'deposit': ['add funds', 'top up', 'transfer in'],
    'withdraw': ['cash out', 'take out', 'transfer out'],
    'balance': ['funds', 'money', 'amount'],
    'invest': ['buy shares', 'purchase shares'],
    'returns': ['earnings', 'profit', 'income'],
    'bonus': ['reward', 'prize', 'gift'],
    'support': ['help', 'assistance', 'customer service'],
    'problem': ['issue', 'error', 'bug', 'trouble'],
}