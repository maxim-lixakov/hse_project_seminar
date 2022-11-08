import React from "react";
import './App.css';
import Circle from 'react-circle';
import {
  SafeAreaView,
  StyleSheet,
  View,
  Image,
  Text, Dimensions, TouchableHighlight,
} from 'react-native';


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
                right: -24000,
                top: -110,
                bottom: 50,
            };
          const { DataisLoaded, items } = this.state;
        if (!DataisLoaded) return <div>
            <h1> Please wait some time.... </h1> </div> ;
          return (
        <div style={myStyle} >
            <View style = {styless.container}>
         <Text style = {styless.text}>
            <Text style = {styless.capitalLetter}>
               Научно исследовательский семинар
            </Text>
         </Text>

      </View>
            <Text style = {styless.data}> UNIQUE PRODUCTS </Text>
            <SafeAreaView style={{flex: 1}}>
                   <TouchableHighlight
      style = {{
        borderRadius: Math.round(Dimensions.get('window').width + Dimensions.get('window').height) / 2,
        width: Dimensions.get('window').width * 0.14,
        height: Dimensions.get('window').width * 0.14,
        backgroundColor:'#ffffff',
        justifyContent: 'center',
        alignItems: 'center'
      }}
      underlayColor = '#ccc'
      onPress = { () => alert('Yaay!') }
    >
      <Text style = {styless.data}> {items.goods} </Text>
    </TouchableHighlight>
                    </SafeAreaView>
            <div style={{float: 'right', padding: 40, left: 100}}>
                    <Text style = {styless.data}> ITEMS COLLECTED </Text>
            <SafeAreaView style={{flex: 1}}>
                   <TouchableHighlight
      style = {{
        borderRadius: Math.round(Dimensions.get('window').width + Dimensions.get('window').height) / 2,
        width: Dimensions.get('window').width * 0.17,
        height: Dimensions.get('window').width * 0.17,
        backgroundColor:'#ffeea9',
        justifyContent: 'center',
        alignItems: 'center',
      }}
      underlayColor = '#ccc'
      onPress = { () => alert('Yaay!') }
    >
      <Text style = {styless.data}> {items.rows} </Text>
    </TouchableHighlight>
                    </SafeAreaView>
                </div>


      <View style={styles.container}>
        <Image
          source={
                require('./img/max.png')
          }
          //borderRadius will help to make Round Shape
          style={{
            width: 200,
            height: 200,
            borderRadius: 200 / 2
          }}
        />
        <Text style={styles.textHeadingStyle}>
          Ликсаков Максим
        </Text>
      </View>
            <SafeAreaView style={{flex: 1}}>
      <View style={styles.container1}>
        <Image
          source={
                require('./img/ilyas.png')
          }
          //borderRadius will help to make Round Shape
          style={{
            width: 200,
            height: 200,
            borderRadius: 200 / 2
          }}
        />
        <Text style={styles.textHeadingStyle}>
          Гасанов Ильяс
        </Text>
      </View>
    </SafeAreaView>
        </div>

          );
        }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
      right: -420,
      bottom: 50,
      top: -160,
  },
    container1: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
      right: -210,
        top: -150,
      bottom: 50,
  },

        container2: {
    flex: 1,
            alignItems: 'center',
    justifyContent: 'center',
      right: -50,
        top: -110,
      bottom: 50,
  },

            container3: {
    flex: 1,
      right: -250,
        top: -110,
      bottom: 50,
  },

  textHeadingStyle: {
    marginTop: 20,
    fontSize: 20,
    color: '#0250a3',
    fontWeight: 'bold',
  },
});


const styless = StyleSheet.create ({
   container: {
      alignItems: 'center',
      padding: 20
   },
   text: {
      color: '#41cdf4',
   },
   capitalLetter: {
      color: 'black',
      fontSize: 30
   },
   wordBold: {
      fontWeight: 'bold',
      color: 'black'
   },
   italicText: {
      color: '#37859b',
      fontStyle: 'italic'
   },
   textShadow: {
      textShadowColor: 'red',
      textShadowOffset: { width: 2, height: 2 },
      textShadowRadius : 5
   },
    data: {
      color: 'purple',
      fontSize: 22,
      fontWeight: 'bold',
        alignItems: 'center',
              padding: 20,
              textShadowOffset: { width: 2, height: 2 },
   }
})

export default App;