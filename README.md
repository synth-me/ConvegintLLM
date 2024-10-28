# ConvegintLLM
GPT-4o driven code assistant for EBO software

# Usage of LLM

After you run the code you need to simply click "Turn On" and now your "crtl+c" is being listened by the AI. 

![image](https://github.com/user-attachments/assets/67886028-aff1-48b0-b440-3e49354b96e2)
![image](https://github.com/user-attachments/assets/2ba7db05-1d8a-4d52-8f81-2cde7f5a9152)

Inside the code editor, you can simply create a prompt that will feed the model with the instructions you want it to follow like: 

```javascript
/* 
    Create a function that will colorize an element using
    color attribute named "Node" with input color
*/
```

And then in your clipboard will be storage the following information: 

```javascript
/* 
    Create a function that will colorize an element using
    color attribute named "Node" with input color
    @param {string} color 
*/
function colorizeElementRed(color) {
    // Get the element with the Name attribute "Element"
    var element = evt.getChild("Element");
    
    // Check if the element exists
    if (element) {
        // Set the color of the element to red in HEX
        element.setAttribute("Color", color);
    }
}
```

# Usage of Code Completion 

We also have an rule based code completion that is based on EBO's function. 
All you need is to use "crtl+q" in a partially completed code like: 

```javascript
node.getElemen
```

and then after clicking "crtl+q" it will select the fittest completion and 
store it into your clipboard 

```javascript
node.getElemenById("<Id>")
```

⚠ Warning ⚠

The prompt engineering behind this it's still on early phases and i created this software to help me with my specific problems so be aware not to use the generated code directly into production systems, it'll probably cause you harm 
Also, be aware that the needed information for the GPT to understand the EBO's API is huge and it consumes a lot of tokens (you can check the token's consumption using the sqlite database that the script generates once you run it). 
