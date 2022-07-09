class Sessions:
    def __init__(self):
        self.sessions = []

    def session_present(self, ip, name):
        return [ip, name] in self.sessions

    def add_session(self, ip, name):
        self.sessions.append([ip, name])

    def get_sessions(self, ip):
        res = []
        for session in self.sessions:
            if session[0] == ip:
                res.append(session[1])

        return res

    def replace_session(self, ip, name, replacement):
        for integer in range(len(self.sessions)):
            if self.sessions[integer] == [ip, name]:
                self.sessions[integer] = [ip, replacement]
                return

    def remove_session(self, ip, name):
        for session in self.sessions:
            if session == [ip, name]:
                self.sessions.remove(session)
                return

    def clear_sessions(self, ip):
        for session in self.sessions:
            if session[0] == ip:
                self.sessions.remove(session)
