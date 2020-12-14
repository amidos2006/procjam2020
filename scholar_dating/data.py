import random

class ConversationMemory:
    def __init__(self, max_size):
        self.memory = []
        self.max_size = max_size

    def add(self, playerText, userText):
        self.memory.append((playerText, userText))
        if len(self.memory) > self.max_size:
            del self.memory[0]

    def prompt(self, player, user):
        result = ""
        for t in self.memory:
            result += player.get_first_name() + ": " + t[0] + " "
            result += user.get_first_name() + ": " + t[1] + " "
        return result

class PaperInfo:
    def __init__(self, name, citations, description):
        self.name = name
        self.description = description
        self.citations = citations

    def get_info(self):
        return self.name + "can be described as: " + self.description

class UserInfo:
    memory_size = 5

    def __init__(self, name, pic, citations, hindex, i10index):
        self.name = name
        self.pic = pic
        self.citations = citations
        self.i10index = i10index
        self.hindex = hindex
        self.job = []
        self.paper = []
        self.interest = []
        self.love = 0
        self.prompt = ""
        self.context = []
        self.memory = ConversationMemory(UserInfo.memory_size)

    def init_pickup_lines(self, engine, size):
        prompt = ""

        f = open('assets/pickup.txt')
        lines = f.readlines()
        f.close()
        random.shuffle(lines)
        for i in range(size):
            # answer = engine.test_gpt2(lines[i])
            # prompt += lines[i] + " " + answer + " "
            lines[i] = lines[i].strip()
            if lines[i][-1] not in [".", "!", "?"]:
                lines[i] = lines[i] + "."
            prompt += lines[i] + " "

        return prompt

    def get_paper_prompts(self):
        return [p.get_info() for p in self.paper]

    def init(self, config, parser, engine, player):
        context = ""
        max_size = 0
        for info in config["fic_info"]:
            context += parser.parse_fic(info["file"], info["size"], player, self) + " "
            max_size += info["size"]
            if max_size >= config["max_fic_size"]:
                self.context.append(context)
                context = ""
                max_size = 0
        self.context.insert(1, self.init_pickup_lines(engine, config["pickup_size"]))
        self.context = self.context + self.get_paper_prompts()
        self.prompt = parser.parse_normal(config["prompt"], player, self)
        print(self.context)
        print(self.prompt)

    def get_first_name(self):
        return self.name.split(' ')[0]

    def get_job(self):
        return ", ".join(self.job)

    def get_interests(self):
        return ", ".join(self.interest)

    def add_job(self, job):
        self.job.append(job)

    def add_paper(self, paper):
        self.paper.append(paper)

    def add_interest(self, interest):
        self.interest.append(interest)

    def get_prompt(self, player, question):
        prompt = self.prompt
        prompt += self.memory.prompt(player, self)
        if question.strip()[-1] not in [".", "!", "?"]:
            question = question.strip() + "."
        prompt += "{}: {} ".format(player.get_first_name(), question)
        prompt += "{}:".format(self.get_first_name())
        return prompt
