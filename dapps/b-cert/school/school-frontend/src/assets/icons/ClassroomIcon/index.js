import { SvgIcon } from "@material-ui/core";
import { ReactComponent as ClassroomSvg } from "./classroom.svg";

export default function ClassroomIcon(props) {
  return (
    <SvgIcon {...props}>
      <ClassroomSvg></ClassroomSvg>
    </SvgIcon>
  );
}
