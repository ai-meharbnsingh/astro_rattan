// Shim for @react-three/fiber and @react-three/drei
// R3F v8 is incompatible with React 19 — stub until upgraded
const noop = () => null;
export const Canvas = noop;
export const useFrame = noop;
export const useThree = () => ({});
export const Stars = noop;
export const Float = noop;
export const Billboard = noop;
export const Text = noop;
export default noop;
