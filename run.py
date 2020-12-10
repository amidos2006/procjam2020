from scholar_dating.engine import ConversationEngine
from scholar_dating.data import UserInfo, PaperInfo
import json

if __name__ == '__main__':
    f = open("assets/config.json")
    config = json.load(f)
    f.close()

    engine = ConversationEngine(config["qa_threshold"], config["top_k"], config["max_length"], config["temperature"], config["repeat_penalty"])
    print('Please wait while models are being loaded.')
    engine.load_pipeline(config["qa_name"], config["qa_folder"], config["gpt2_name"], config["gpt2_folder"])

    player = UserInfo("Julian Togelius", None, 13501, 61, 225)
    player.add_job("Associate Professor of Computer Science and Engineering, New York University; co-founder, modl.ai")
    player.add_interest("Artificial Intelligence")
    player.add_interest("Games")
    player.add_interest("Evolutionary Computation")
    player.add_interest("Game AI")
    player.add_interest("Procedural Content Generation")

    user = UserInfo("Sebastian Risi", None, 2207, 27, 53)
    user.init(engine, player, config["pickup_size"])
    user.add_job("Professor, IT University of Copenhagen")
    user.add_interest("Artificial Intelligence")
    user.add_interest("Neural Networks")
    user.add_interest("Neuroevolution")
    user.add_interest("Artificial Life")
    user.add_paper(PaperInfo("Neuroevolution in games: State of the art and open challenges", 108, "This paper surveys research on applying neuroevolution (NE) to games. In neuroevolution, artificial neural networks are trained through evolutionary algorithms, taking inspiration from the way biological brains evolved. We analyze the application of NE in games along five different axes, which are the role NE is chosen to play in a game, the different types of neural networks used, the way these networks are evolved, how the fitness is determined and what type of input the network receives. The paper also highlights important open research challenges in the field."))
    user.add_paper(PaperInfo("Evolving mario levels in the latent space of a deep convolutional generative adversarial network", 100, "Generative Adversarial Networks (GANs) are a machine learning approach capable of generating novel example outputs across a space of provided training examples. Procedural Content Generation (PCG) of levels for video games could benefit from such models, especially for games where there is a pre-existing corpus of levels to emulate. This paper trains a GAN to generate levels for Super Mario Bros using a level from the Video Game Level Corpus. The approach successfully generates a variety of levels similar to one in the original corpus, but is further improved by application of the Covariance Matrix Adaptation Evolution Strategy (CMA-ES). Specifically, various fitness functions are used to discover levels within the latent space of the GAN that maximize desired properties. Simple static properties are optimized, such as a given distribution of tile types. Additionally, the champion A* agent from the 2009 …"))
    # user.add_paper(PaperInfo("Deep learning for video game playing", 99, "In this paper, we review recent deep learning advances in the context of how they have been applied to play different types of video games such as first-person shooters, arcade games, and real-time strategy games. We analyze the unique requirements that different game genres pose to a deep learning system and highlight important open challenges in the context of applying these machine learning methods to video games, such as general game playing, dealing with extremely large decision spaces and sparse rewards."))

    print()
    print("You are {} and you are having a conversation with {}.".format(player.name, user.name))
    print()
    print("If you want to exit at any time just write exit, otherwise chat with {}.".format(user.name))
    print()
    while True:
        question = input("{}: ".format(player.get_first_name()))
        if question.lower().strip() == "exit":
            break
        answer = engine.get_response(player, user, question)
        print()
        print("{}: {}".format(user.get_first_name(), answer))
        print()
