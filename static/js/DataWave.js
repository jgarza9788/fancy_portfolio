function ready(callback){
    // in case the document is already rendered
    if (document.readyState!='loading') callback();
    // modern browsers
    else if (document.addEventListener) document.addEventListener('DOMContentLoaded', callback);
    // IE <= 8
    else document.attachEvent('onreadystatechange', function(){
        if (document.readyState=='complete') callback();
    });
}

ready(function(){

import \* as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r120/three.min.js';

let renderer,
    camera,
    planet,
    moon,
    sphereBg,
    terrainGeometry,
    container = document.getElementById("canvas_container"),
    timeout_Debounce,
    frame = 0,
    cameraDx = 0.05,
    count = 0,
    t = 0;

const d = new Date(); 
count = d.getMinutes()

/*   Lines values  */
let lineTotal = 1000;
let linesGeometry = new THREE.BufferGeometry();
linesGeometry.setAttribute("position", new THREE.BufferAttribute(new Float32Array(6 * lineTotal), 3));
linesGeometry.setAttribute("velocity", new THREE.BufferAttribute(new Float32Array(2 * lineTotal), 1));
let l_positionAttr = linesGeometry.getAttribute("position");
let l_vertex_Array = linesGeometry.getAttribute("position").array;
let l_velocity_Array = linesGeometry.getAttribute("velocity").array;


init();
animate();


function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color("#000000");
    scene.fog = new THREE.Fog("#3c1e02", 0.5, 50);

    camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.01, 1000)
    camera.position.set(0, 1, 32)

//     pointLight1 = new THREE.PointLight("#ffffff", 1, 0);
//     pointLight1.position.set(0, 30, 30);
//     pointLight1.castShadow = true; // default false
//     scene.add(pointLight1);
  
//     //Set up shadow properties for the light
//     pointLight1.shadow.mapSize.width = 512; // default
//     pointLight1.shadow.mapSize.height = 512; // default
//     pointLight1.shadow.camera.near = 0.5; // default
//     pointLight1.shadow.camera.far = 500; // default
  
//     const helper = new THREE.CameraHelper( pointLight1.shadow.camera );
//     scene.add( helper );

    renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true
    });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    const loader = new THREE.TextureLoader();


    // // Sphere Background 
    // const textureSphereBg = loader.load('https://i.ibb.co/JCsHJpp/stars2-qx9prz.jpg');
    // textureSphereBg.anisotropy = 16;
    // const geometrySphereBg = new THREE.SphereBufferGeometry(150, 32, 32);
    // const materialSphereBg = new THREE.MeshBasicMaterial({
    //     side: THREE.BackSide,
    //     map: textureSphereBg,
    //     fog: false
    // });
    // sphereBg = new THREE.Mesh(geometrySphereBg, materialSphereBg);
    // sphereBg.position.set(0, 50, 0);
    // scene.add(sphereBg);
  

    // Terrain
    /*
    const textureTerrain = loader.load();
    textureTerrain.rotation = THREE.MathUtils.degToRad(5);
    terrainGeometry = new THREE.PlaneBufferGeometry(70, 70, 20, 20);
    const terrainMaterial = new THREE.MeshBasicMaterial({
        map: textureTerrain,
        fog: true
    });
    terrain = new THREE.Mesh(terrainGeometry, terrainMaterial);
    terrain.rotation.x = -0.15 * Math.PI;
    // terrain.rotation.z = THREE.Math.degToRad(90);
    scene.add(terrain);
    */
  
    // Terrain
    const textureTerrain = loader.load();
    textureTerrain.rotation = THREE.MathUtils.degToRad(5);
  
    terrainGeometry = new THREE.PlaneBufferGeometry(50, 50, 30, 20);
  
    let t_vertex_Array = terrainGeometry.getAttribute("position").array;
    terrainGeometry.getAttribute("position").setUsage(THREE.DynamicDrawUsage);
  
    terrainGeometry.setAttribute("myZ", new THREE.BufferAttribute(new Float32Array(t_vertex_Array.length / 3), 1));
    let t_myZ_Array = terrainGeometry.getAttribute("myZ").array;

    for (let i = 0; i < t_vertex_Array.length; i++) {
        t_myZ_Array[i] = THREE.MathUtils.randInt(0, 5);
    }
  
    const terrainMaterial = new THREE.MeshBasicMaterial({
        map: textureTerrain,
        color: "#ff",
        wireframe: true, 
        // wireframeLinewidth: 5.0, 
        // wireframeLineCap: "round",
        fog: false,
    });
  
    terrain = new THREE.Mesh(terrainGeometry, terrainMaterial);
    // terrain.castShadow = true;
    // terrain.receiveShadow = true;
    // terrain.rotation.x = -0.15 * Math.PI;
  
    terrain.rotation.x = -0.10 * Math.PI;
    // terrain.rotation.x = -0.3 * Math.PI;
  
    terrain.rotation.z = THREE.Math.degToRad( count*90 );
    terrain.position.set(0, 10, 0)
    scene.add(terrain);
  

  
  
    /*
    let t_vertex_Array = terrainGeometry.getAttribute("position").array;
    terrainGeometry.getAttribute("position").setUsage(THREE.DynamicDrawUsage);

    terrainGeometry.setAttribute("myZ", new THREE.BufferAttribute(new Float32Array(t_vertex_Array.length / 3), 1));
    let t_myZ_Array = terrainGeometry.getAttribute("myZ").array;

    for (let i = 0; i < t_vertex_Array.length; i++) {
        t_myZ_Array[i] = THREE.MathUtils.randInt(0, 5);
    }
  
    const terrain_line = new THREE.LineSegments(
        terrainGeometry,

        new THREE.LineBasicMaterial({
            color: "#0000",
            linewidth: 1.0,
            fog: false,
        })
        
    );
    terrain_line.rotation.x = -0.15 * Math.PI;
    // terrain_line.rotation.z = THREE.Math.degToRad(90);
    scene.add(terrain_line);
    */

  // noise.seed(Math.random());

}


function animate() {


    // Terrain Animation  
    // /*
    let t_vertex_Array = terrainGeometry.getAttribute("position").array;
    let t_myZ_Array = terrainGeometry.getAttribute("myZ").array;
    
    for (let i = 0; i < t_vertex_Array.length; i++) {
        /*
        if (i >= 210 && i <= 250) t_vertex_Array[i * 3 + 2] = 0;
        else {
            t_vertex_Array[i * 3 + 2] = Math.sin((i + count * 0.0003)) * (t_myZ_Array[i] - (t_myZ_Array[i] * 0.75));
            count += 0.01;
        }
        */
      
      // t_vertex_Array[i * 3 + 2] = Math.sin((i + count * 0.0003)) * (t_myZ_Array[i] - (t_myZ_Array[i] * 0.75));
      // t_vertex_Array[i * 3 + 2] = Math.sin( ( (i*0.195) + (count * 1)  )  );
      t_vertex_Array[i * 3 + 2] = Math.sin( ( (i*0.2) + (count * 1)  )  );
      
      
      // t_vertex_Array[i * 3 + 2] = Math.tan( ( (i*0.195) + (count * 1)  )  );
      count += 0.00001;
    }
    // */


    //Camera Movement
    /*
    camera.rotation.z += 0.01
    camera.position.x += cameraDx;
    camera.position.y = -1.2 * (1 - Math.abs(frame / 2000 - 0.5) / 0.5);
    camera.lookAt(0, 0, 0);
    frame += 8;
    if (frame > 2000) frame = 0;
    if (camera.position.x > 18) cameraDx = -cameraDx;
    if (camera.position.x < -18) cameraDx = Math.abs(cameraDx);
    */
  
    terrainGeometry.attributes.position.needsUpdate = true;
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
    
}



/*     Resize     */
window.addEventListener("resize", () => {
    clearTimeout(timeout_Debounce);
    timeout_Debounce = setTimeout(onWindowResize, 80);
});
function onWindowResize() {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}






})
