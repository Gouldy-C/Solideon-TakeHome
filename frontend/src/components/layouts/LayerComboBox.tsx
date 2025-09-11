import { useMemo, useState } from "react";
import { Button } from "../ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../ui/popover";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "../ui/command";
import { ScrollArea } from "../ui/scroll-area";
import { Check, ChevronsUpDown } from "lucide-react";
import type { Layer } from "../../lib/types";

type Props = {
  layers: Layer[];
  selectedLayerId?: string;
  onChange: (id: string) => void;
  disabled?: boolean;
};

function labelForLayer(layer: Layer): string {
  const n = layer.layer_number;
  if (typeof n === "number") return `Layer ${n}`;
  return String(layer.id);
}

export function LayerComboBox(props: Props) {
  const { layers, selectedLayerId, onChange, disabled } = props;
  const [open, setOpen] = useState(false);

  const selectedLabel = useMemo(() => {
    const found = layers.find((l) => l.id === selectedLayerId);
    return found ? labelForLayer(found) : "Select layer";
  }, [layers, selectedLayerId]);

  return (
    <div className="flex items-center gap-3">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between"
            disabled={disabled}
          >
            <span className="truncate">{selectedLabel}</span>
            <ChevronsUpDown className="ml-2 h-4 w-4 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-[320px] p-0">
          <Command>
            <CommandInput placeholder="Search layers…" />
            <ScrollArea>
              <CommandList>
                <CommandEmpty>No layers found.</CommandEmpty>
                <CommandGroup>
                  {layers.map((layer) => (
                    <CommandItem
                      key={layer.id}
                      value={labelForLayer(layer)}
                      onSelect={() => {
                        onChange(layer.id);
                        setOpen(false);
                      }}
                    >
                      <Check
                        className={
                          "mr-2 h-4 w-4 " +
                          (selectedLayerId === layer.id
                            ? "opacity-100"
                            : "opacity-0")
                        }
                      />
                      <span className="truncate">{labelForLayer(layer)}</span>
                    </CommandItem>
                  ))}
                </CommandGroup>
              </CommandList>
            </ScrollArea>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}