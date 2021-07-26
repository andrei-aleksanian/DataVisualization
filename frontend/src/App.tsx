import {useEffect, useState} from 'react';

type HelloWorld = {
  "Hello": string
}

function App() {
  const [hi, setHi] = useState({"Hello": "doesn't work :("});
  useEffect(() => {
    const getStuff = async () => {
      const res = await fetch("http://localhost:8080/test");
      const data: HelloWorld = await res.json();
      setHi(data);
    }
    getStuff();
  }, [])

  return (
    <div className="App">
      <div>If I am saying hello world, I am working:</div>
      <div>Hello {hi["Hello"]}</div>
    </div>
  );
}

export default App;
