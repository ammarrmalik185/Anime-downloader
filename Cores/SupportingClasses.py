class Options:

    def __init__(self, silent=True, quality=None, confirmation=False, logs=False,
                 alternate_quality=True, download_path="\\animes", pages_to_scan=1, auto_exit=False,
                 auto_exception_control=True, max_refresh_page=5, generate_log_file=True, timeout=30):
        if quality is None:
            quality = {"type": "force_res", "value": "720p"}
        self.silent = silent
        self.confirmation = confirmation
        self.logs = logs
        self.quality = quality
        self.alternate_quality = alternate_quality
        self.download_path = download_path
        self.pages_to_scan = pages_to_scan
        self.auto_exit = auto_exit
        self.auto_exception_control = auto_exception_control
        self.max_refresh_page = max_refresh_page
        self.generate_log_file = generate_log_file
        self.timeout = timeout

