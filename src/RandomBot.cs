using ScriptsOfTribute;
using ScriptsOfTribute.AI;
using ScriptsOfTribute.Board;
using ScriptsOfTribute.Serializers;

namespace Bots;

public class RandomBot : AI
{
    private readonly SeededRandom rng = new(123);

    public override PatronId SelectPatron(List<PatronId> availablePatrons, int round)
        => availablePatrons.PickRandom(rng);

    public override Move Play(GameState gameState, List<Move> possibleMoves, TimeSpan remainingTime)
    {
        var move = possibleMoves.PickRandom(rng);
        return move;
    }

    public override void GameEnd(EndGameState state, FullGameState? finalBoardState)
    {
    }
}
