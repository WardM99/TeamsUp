import { useEffect, FormEvent, useState } from 'react'
import axios from 'axios';
import Form from "react-bootstrap/Form";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css'

function PlayersLogin() {
	const [name, setName] = useState("");
	const [password, setPassword] = useState("");

	async function handleSubmit(event: FormEvent) {
		event.preventDefault();
		const data = {"username": name, "password": password, "grant_type": "password"};
		const config = {
			headers: {
				"content-type": "application/x-www-form-urlencoded"
			}
		}
		axios.post("http://localhost:8000/players/login", data, config)
			.then(response => {
				console.log(response.data)
			})
			.catch(error =>{
				console.log(error)
			})

		/*
			"https://localhost:8000/players/login",
			{"username": name, "password": password, "grant_type": "password"},
			{headers:{"content-type": "application/x-www-form-urlencoded"}}
		*/
		
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
			<Button variant="primary" type="submit">Submit</Button>
		</Form>
    )
}

export default PlayersLogin