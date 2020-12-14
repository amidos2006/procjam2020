import random

class Parser:
    def __init__(self, engine):
        self.engine = engine

    def parse_line(self, line, player, user):
        line = line.strip()
        line = line.replace("{user.name}", user.name)
        line = line.replace("{user.first_name}", user.get_first_name())
        line = line.replace("{user.job}", user.get_job())
        line = line.replace("{user.interests}", user.get_interests())
        line = line.replace("{user.citations}", str(user.citations))
        line = line.replace("{user.hindex}", str(user.hindex))
        line = line.replace("{user.i10index}", str(user.i10index))

        line = line.replace("{player.name}", player.name)
        line = line.replace("{player.first_name}", player.get_first_name())
        line = line.replace("{player.job}", player.get_job())
        line = line.replace("{player.interests}", player.get_interests())
        line = line.replace("{player.citations}", str(player.citations))
        line = line.replace("{player.hindex}", str(player.hindex))
        line = line.replace("{player.i10index}", str(player.i10index))

        return line

    def parse_fic(self, file, size, player, user):
        result = ""
        f = open(file)
        lines = f.readlines()
        random.shuffle(lines)
        f.close()
        for i in range(size):
            l = lines[i]
            input = self.parse_line(l, player, user)
            output = self.engine.test_gpt2(input)
            if len(output) == 0:
                result += input + ". "
            else:
                result += input + " " + output + " "
        return result.replace("\n", " ").strip()

    def parse_normal(self, file, player, user):
        result = ""
        f = open(file)
        lines = f.readlines()
        f.close()
        for l in lines:
            result += self.parse_line(l, player, user)
        return result.replace("\n", " ").strip()
