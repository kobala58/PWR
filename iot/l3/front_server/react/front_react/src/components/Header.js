import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function Header() {
    return (
        <Navbar bg="light" expand="lg">
            <Container>
                <Navbar.Brand href="#home">IoT + Docker</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="#home">Services</Nav.Link>
                        <Nav.Link href="#add">Dodaj nowy</Nav.Link>
                        <NavDropdown title="Inne" id="basic-nav-dropdown">
                            <NavDropdown.Item href="#action/3.1">Github</NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.2">
                                Opisy zadań
                            </NavDropdown.Item>
                            <NavDropdown.Item href="#action/3.3">Schemat na kartce</NavDropdown.Item>
                            <NavDropdown.Divider />
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}

export default Header