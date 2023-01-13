interface Props {
  playerName: string;
}

function PlayersInfo(props: Props) {
  return <span data-testid="PlayersInfoId">{props.playerName}</span>;
}

export default PlayersInfo;
