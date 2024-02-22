import Actor, Player

def main():
    #Player = player.Player("Илюха")
    #Player.getInfo()

    Petya = Actor.Actor("Petya", 1)

    print(Petya.calculateDamage(Petya))

    Petya.giveExperience(1000)
    if not (Petya.takeDamage(100)):
        del(Petya)


if __name__ == '__main__':
    main()