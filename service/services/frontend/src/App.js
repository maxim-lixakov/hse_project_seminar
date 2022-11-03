import React from "react";
import './App.css';
import Circle from 'react-circle';



class App extends React.Component {

    // Constructor
    constructor(props) {
        super(props);

        this.state = {
            items: [],
            DataisLoaded: false
        };
    }

    // ComponentDidMount is used to
    // execute the code
    componentDidMount() {
        fetch(
"http://localhost:1337/api/data_info")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    items: json,
                    DataisLoaded: true
                });
            })
    }
    render() {
          const myStyle={
                backgroundImage: "url(/img/image.png)",
                height:'100vh',
                fontSize:'50px',
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
            };
          const { DataisLoaded, items } = this.state;
        if (!DataisLoaded) return <div>
            <h1> Please wait some time.... </h1> </div> ;
          return (
        <div style={myStyle} >

<Circle
    size={170}
    showPercentageSymbol={false}
  progress={items.rows}
/>
        </div>
          );
        }
}

export default App;