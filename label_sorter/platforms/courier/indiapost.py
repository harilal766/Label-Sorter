from base_label import BaseLabel




class IndiapostLabel(BaseLabel):
    TRACKING_ID_PATTERN = r'EY\d{9}IN'
    
    