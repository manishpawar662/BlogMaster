// script.js 
let password = document.getElementById("password"); 
let power = document.getElementById("power-point"); 

if (password){
password.oninput = function () { 
    let point = 0; 
    let value = password.value; 
    let widthPower =  
        ["1%", "25%", "50%", "75%", "100%"]; 
    let colorPower =  
        ["#D73F40", "#DC6551", "#F2B84F", "#BDE952", "#3ba62f"]; 
  
    if (value.length >= 6) { 
        let arrayTest =  
            [/[0-9]/, /[a-z]/, /[A-Z]/, /[^0-9a-zA-Z]/]; 
        arrayTest.forEach((item) => { 
            if (item.test(value)) { 
                point += 1; 
            } 
        }); 
    } 
    power.style.width = widthPower[point]; 
    power.style.backgroundColor = colorPower[point]; 
};
}

console.log("working")
let addflag = null;
function showcomments(user,sno) {
    console.log(user,sno);
    let div = document.getElementById(sno)
    // document.getElementById("myDropdown").classList.toggle("show");
    if(div.style.display == "none" && addflag==null){
        div.style.display = "block";
        // form.style.opacity = 1;
        console.log("add showing");
        console.log("if",addflag);
    }
    else{
        div.style.display = "none";
        // form.style.opacity = 0;
        console.log("add removed");
        console.log("else",addflag);
    }
}