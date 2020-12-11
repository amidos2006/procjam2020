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

    def init_personal_info(self, engine, player):
        prompt = ""

        input = "Hello {}".format(player.get_first_name())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + "! "
        else:
            prompt += input + " " + output + " "

        input = "My name is {}".format(self.name)
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        input = "I am a {}".format(self.get_job())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        input = "I have {} citations".format(self.citations)
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        input = "I am interested in {}".format(self.get_interests())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        return prompt

    def init_fiction_info(self, engine):
        prompt = ""

        # input = "I work as {} that is why I live in".format(self.get_job())
        # output = engine.test_gpt2(input)
        # if len(output) == 0:
        #     prompt += input + ". "
        # else:
        #     prompt += input + " " + output + " "

        input = "I hate you like a bad paper because".format(self.get_job())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        input = "I dislike you and your papers because".format(self.get_job())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        input = "I like you like an IJCAI paper because".format(self.get_job())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        input = "I love you because you are as classic as AAAI paper because".format(self.get_job())
        output = engine.test_gpt2(input)
        if len(output) == 0:
            prompt += input + ". "
        else:
            prompt += input + " " + output + " "

        # input = "I age quickly and wisely like NIPs paper because"
        # output = engine.test_gpt2(input)
        # if len(output) == 0:
        #     prompt += input + ". "
        # else:
        #     prompt += input + " " + output + " "

        return prompt

    def init_pickup_lines(self, engine, size):
        prompt = ""

        f = open('assets/pickup.txt')
        lines = f.readlines()
        f.close()
        random.shuffle(lines)
        for i in range(size):
            # answer = engine.test_gpt2(lines[i])
            # prompt += lines[i] + " " + answer + " "
            if lines[i].strip()[-1] not in [".", "!", "?"]:
                lines[i] = lines[i].strip() + "."
            prompt += lines[i] + " "

        return prompt

    def init_prompt(self, player):
        prompt = ""
        prompt += "{} is interested in {}. ".format(self.get_first_name(), self.get_interests())
        prompt += "They work as {}. ".format(self.get_job())
        prompt += "They have {} citations, {} hindex, and {} i10index".format(self.citations, self.hindex, self.i10index)
        prompt += "In a conversation between {} and {}. ".format(player.get_first_name(), self.get_first_name())
        # prompt += "{}: Hello, how are you? ".format(player.get_first_name())
        # prompt += "{}: I am fine what about you. ".format(self.get_first_name())
        # prompt += "{}: What do you do for living? ".format(player.get_first_name())
        # prompt += "{}: I am a {}. ".format(self.get_first_name(), self.get_job())
        # prompt += "{}: What are your interests? ".format(player.get_first_name())
        # prompt += "{}: I am interested into {}. ".format(self.get_first_name(), self.get_interests())
        return prompt

    def init(self, engine, player, size):
        self.context.append(self.init_personal_info(engine, player))
        self.context.append(self.init_pickup_lines(engine, size))
        self.context.append(self.init_fiction_info(engine))
        self.context = self.context + self.get_paper_prompts()
        self.prompt = self.init_prompt(player)

    def get_first_name(self):
        return self.name.split(' ')[0]

    def get_job(self):
        return ", ".join(self.job)

    def get_interests(self):
        return ",".join(self.interest)

    def get_pickup(self):
        return " ".join(self.pickup)

    def add_job(self, job):
        self.job.append(job)

    def add_paper(self, paper):
        self.paper.append(paper)

    def add_interest(self, interest):
        self.interest.append(interest)

    def get_paper_prompts(self):
        return [p.get_info() for p in self.paper]

    def get_prompt(self, player, question):
        prompt = self.prompt
        prompt += self.memory.prompt(player, self)
        if question.strip()[-1] not in [".", "!", "?"]:
            question = question.strip() + "."
        prompt += "{}: {} ".format(player.get_first_name(), question)
        prompt += "{}:".format(self.get_first_name())
        return prompt
