import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import PlayersInfo from "../players/PlayersInfo";
import { logout } from "../../utils/api/player";
import { Player } from "../../data/interfaces";

interface Props {
  player: Player | undefined;
  isLoggedIn: boolean;
  setIsLoggedIn: (value: boolean) => void;
}

function NavBar(props: Props) {
  function logoutAndRedirect() {
    logout();
    props.setIsLoggedIn(false);
  }

  if (!props.isLoggedIn || props.player === undefined) return <div></div>;

  return (
    <Navbar bg="light" expand="lg" data-testid="NavBarId">
      <Container>
        <Navbar.Brand href="/">
          <PlayersInfo playerName={props.player.name} />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link href="#home">Home</Nav.Link>
            <Nav.Link href="#link">Link</Nav.Link>
          </Nav>
          <Button
            data-testid="LogOutButtonId"
            variant="danger"
            onClick={logoutAndRedirect}
          >
            Log out
          </Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default NavBar;
