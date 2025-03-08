function [matlablines] = pytomatlinedict(pylisdict)
    %I literally copied this function from ChatGPT cause I can't be asked
    %to code it
    matlablines = repmat(struct('busfrom', 0, 'busto', 0, 'connumber', 0, 'leninbox', 0), length(pylisdict{1}), 1);
    for k = 1:length(pylisdict{1})
        pydict = pylisdict{1}{k};
        matlablines(k).busfrom = double(pydict{'busfrom'});
        matlablines(k).busto = double(pydict{'busto'});
        % I don't really need the locations of the TL's (I'm not storing
        % them for the buses)
        %matlablines(k).from = cell(pydict{'from'});  
        %matlablines(k).to = cell(pydict{'to'});      
        matlablines(k).connumber = double(pydict{'connumber'});
        matlablines(k).leninbox = double(pydict{'leninbox'});
    end

end