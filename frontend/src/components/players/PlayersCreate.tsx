import { FormEvent, useState } from 'react'
import { useNavigate } from "react-router-dom";
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css'
import { createPlayer } from '../../utils/api/player';

function PlayersCreate() {
    const [name, setName] = useState("");
	const [password, setPassword] = useState("");
    const navigate = useNavigate();

	async function handleSubmit(event: FormEvent) {
		event.preventDefault();
		const loginCode = await createPlayer(name, password);
		if(loginCode == 201){
			navigate("/");
		}
		
	}

    return (
		<Form onSubmit={handleSubmit}>
			<Form.Group controlId="formBasicName">
				<Form.Label>Name</Form.Label>
				<Form.Control type="text" placeholder="Enter name" onChange={e => setName(e.target.value)} required/>
			</Form.Group>

			<Form.Group controlId="formBasicPassword">
				<Form.Label>Password</Form.Label>
				<Form.Control type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} required/>
			</Form.Group>
			<Button variant="primary" type="submit">Create</Button>
            <a href="/login">Login</a>
		</Form>
    )
}

export default PlayersCreate