import { Box, Button, Paper, TextField } from "@material-ui/core";

export default function InputClassId({ classId, setClassId, hdGetClass }) {
  return (
    <Paper>
      <Box px={2} py={2} display="flex" alignItems="flex-end">
        <TextField
          label="Mã lớp"
          InputLabelProps={{ shrink: true }}
          autoFocus
          value={classId}
          onChange={(e) => setClassId(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              hdGetClass();
            }
          }}
        ></TextField>
        <Box px={2}>
          <Button variant="contained" color="primary" onClick={hdGetClass}>
            Go
          </Button>
        </Box>
      </Box>
    </Paper>
  );
}
