import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import KnowledgeAgent from './components/KnowledgeAgent';
import './styles/main.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={KnowledgeAgent} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;