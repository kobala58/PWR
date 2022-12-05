import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import HomeScreen from "./screens/HomeScreen";
import Header from "./components/Header";

function App() {
  return (
      <main className="py-3">
      <Header/>
        <HomeScreen />
      </main>
  )
}

export default App;
