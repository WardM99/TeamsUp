import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import PlayersInfo from "../players/PlayersInfo";
import { logout } from "../../utils/api/player";

function NavBar() {
  const navigate = useNavigate();

  function logoutAndRedirect() {
    logout();
    navigate("/login");
  }
  return (
    <Navbar bg="light" expand="lg" data-testid="NavBarId">
      <Container>
        <Navbar.Brand href="/">
          <PlayersInfo />
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
