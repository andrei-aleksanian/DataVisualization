import * as React from 'react';
import { extend, useThree, useFrame, ReactThreeFiber } from '@react-three/fiber';
import { TrackballControls } from 'three/examples/jsm/controls/TrackballControls';
import * as THREE from 'three';

extend({ TrackballControls });

// https://spectrum.chat/react-three-fiber/general/property-orbitcontrols-does-not-exist-on-type-jsx-intrinsicelements~44712e68-4601-4486-b4b4-5e112f3dc09e
// Messy solution to avoid the typescript compiler compplaining about types here
declare global {
  namespace JSX {
    interface IntrinsicElements {
      trackballControls: ReactThreeFiber.Object3DNode<TrackballControls, typeof TrackballControls>;
    }
  }
}

interface TrackballRef {
  update: Function;
}

const Controls = () => {
  const controls = React.useRef<TrackballRef>(null);
  const { camera, gl } = useThree();

  useFrame(() => {
    // update the view as the vis is interacted with
    controls.current?.update();
  });

  return (
    <trackballControls
      ref={controls}
      args={[camera, gl.domElement]}
      dynamicDampingFactor={0.1}
      mouseButtons={{
        LEFT: THREE.MOUSE.PAN, // make pan the default instead of rotate
        MIDDLE: THREE.MOUSE.MIDDLE,
        RIGHT: THREE.MOUSE.ROTATE,
      }}
    />
  );
};

export default Controls;
