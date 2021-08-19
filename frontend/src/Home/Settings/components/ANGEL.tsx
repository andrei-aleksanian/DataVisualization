import Slider from 'Components/Forms/Slider';

import CheckBoxes from 'Components/Forms/CheckBoxes';

export const H1_TEXT = 'Example: Cylinder';

enum FlagMove {
  ON,
  OFF,
}

interface SettingsANGEL {
  neighbour: number;
  lambda: number;
  alpha: number;
  sparsity: number;
  epsilon: number;
  flagMove: FlagMove;
}

export const defaultSettingsANGEL: SettingsANGEL = {
  neighbour: 10,
  lambda: 0,
  alpha: 0,
  sparsity: 0.05,
  epsilon: 0.1,
  flagMove: FlagMove.OFF,
};
export interface SettingsANGELProps {
  settingsANGEL: SettingsANGEL;
  setSettingsANGEL: React.Dispatch<React.SetStateAction<SettingsANGEL>>;
}

const ANGEL = ({ settingsANGEL, setSettingsANGEL }: SettingsANGELProps) => {
  const onChangeNeighbour = (value: number) => setSettingsANGEL((prev) => ({ ...prev, neighbour: value }));
  const onChangeLambda = (value: number) => setSettingsANGEL((prev) => ({ ...prev, lambda: value }));
  const onChangeSparsity = (value: number) => setSettingsANGEL((prev) => ({ ...prev, sparsity: value }));
  const onChangeEpsilon = (value: number) => setSettingsANGEL((prev) => ({ ...prev, epsilon: value }));

  const onChangeFlagMove = (event: React.ChangeEvent, value: FlagMove) => {
    event.preventDefault();
    setSettingsANGEL((prev) => ({ ...prev, flagMove: value }));
  };

  return (
    <>
      <Slider
        min={10}
        max={100}
        step={10}
        marksArr={[10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
        onChange={onChangeNeighbour}
        text="Neighbour"
        value={settingsANGEL.neighbour}
      />
      <Slider
        min={0}
        max={1}
        step={0.2}
        marksArr={[0, 0.2, 0.4, 0.6, 0.8, 1]}
        onChange={onChangeLambda}
        text="Lambda"
        value={settingsANGEL.lambda}
      />
      <Slider
        min={0.05}
        max={0.2}
        step={null}
        marksArr={[0.05, 0.1, 0.2]}
        onChange={onChangeSparsity}
        text="Sparsity"
        value={settingsANGEL.sparsity}
      />
      <Slider
        min={0.1}
        max={1}
        step={null}
        marksArr={[0.1, 0.5, 1]}
        onChange={onChangeEpsilon}
        text="Epsilon"
        value={settingsANGEL.epsilon}
      />
      <CheckBoxes
        heading="Flag move:"
        currentValue={settingsANGEL.flagMove}
        onChange={onChangeFlagMove}
        entries={[
          { value: FlagMove.OFF, text: '0' },
          { value: FlagMove.ON, text: '1' },
        ]}
      />
    </>
  );
};

export default ANGEL;
