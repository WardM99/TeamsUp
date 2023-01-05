<<<<<<< HEAD:frontend/src/players/PlayersLogin.tsx
import { FormEvent, useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css";

function PlayersLogin() {
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    alert(name + " " + password);
  }
=======
import { FormEvent, useState } from 'react'
import { useNavigate } from "react-router-dom";
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css'
import { login } from '../../utils/api/player';

function PlayersLogin() {
	const [name, setName] = useState("");
	const [password, setPassword] = useState("");
    const navigate = useNavigate();

	async function handleSubmit(event: FormEvent) {
		event.preventDefault();
		const loginCode = await login(name, password);
		if(loginCode === 200){
			navigate("/");
		}
		
	}
>>>>>>> master:frontend/src/components/players/PlayersLogin.tsx

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group controlId="formBasicName">
        <Form.Label>Name</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter name"
          onChange={(e) => setName(e.target.value)}
          required
        />
      </Form.Group>

<<<<<<< HEAD:frontend/src/players/PlayersLogin.tsx
      <Form.Group controlId="formBasicPassword">
        <Form.Label>Password</Form.Label>
        <Form.Control
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </Form.Group>
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  );
=======
			<Form.Group controlId="formBasicPassword">
				<Form.Label>Password</Form.Label>
				<Form.Control type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} required/>
			</Form.Group>
			<Button variant="primary" type="submit">Login</Button>
			<Button variant="link" href="/register">Register</Button>
		</Form>
    )
>>>>>>> master:frontend/src/components/players/PlayersLogin.tsx
}

export default PlayersLogin;
